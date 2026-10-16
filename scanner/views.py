from django.shortcuts import render
from scanner.models import QRcode
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from pathlib import Path
from django.utils.text import slugify
import qrcode
import cv2
import numpy as np
from PIL import Image


def generate_qr(request):
    qr_image_url = None

    if request.method == "POST":
        mobile_number = request.POST.get('mobile_number')
        data = request.POST.get('qr_data')

        if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
            return render(request, 'scanner/generate.html', {
                'error': 'Invalid mobile number'
            })

        if not data or not data.strip():
            return render(request, 'scanner/generate.html', {
                'error': 'QR data is required'
            })

        data = data.strip()

        # Generate QR code
        qr_content = f"{data}|{mobile_number}"
        qr = qrcode.make(qr_content)

        qr_image_io = BytesIO()
        qr.save(qr_image_io, format='PNG')
        qr_image_io.seek(0)

        # Set storage path
        qr_storage_path = Path(settings.MEDIA_ROOT) / 'qr_codes'
        fs = FileSystemStorage(
            location=qr_storage_path,
            base_url='/media/qr_codes/'
        )

        safe_data = slugify(data)[:50] or 'qr'
        file_name = f"{safe_data}_{mobile_number}.png"

        qr_image_content = ContentFile(
            qr_image_io.read(),
            name=file_name
        )

        file_path = fs.save(file_name, qr_image_content)
        qr_image_url = fs.url(file_path)

        # Save QR data in database
        QRcode.objects.create(
            data=data,
            mobile_number=mobile_number
        )

    return render(request, 'scanner/generate.html', {
        'qr_image_url': qr_image_url
    })


def scan_qr(request):
    result = None
    qr_image_path = None
    generated_qr_path = None

    if request.method == "POST":
        mobile_number = request.POST.get('mobile_number')
        qr_image = request.FILES.get('qr_image')

        if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
            return render(request, 'scanner/scan.html', {
                'error': 'Invalid mobile number'
            })

        if not qr_image:
            return render(request, 'scanner/scan.html', {
                'error': 'Please upload a QR image'
            })

        # Save uploaded image
        upload_storage_path = Path(settings.MEDIA_ROOT) / 'uploads'
        fs = FileSystemStorage(location=upload_storage_path)
        filename = fs.save(qr_image.name, qr_image)
        qr_image_path = upload_storage_path / filename

        try:
            # Read image using OpenCV for reliable decoding without DLL dependencies
            img_cv = cv2.imread(str(qr_image_path))
            
            if img_cv is None:
                # Fallback if cv2 cannot read it directly, use PIL to convert
                pil_img = Image.open(qr_image_path).convert('RGB')
                img_cv = np.array(pil_img)
                img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

            detector = cv2.QRCodeDetector()
            qr_content, bbox, straight_qrcode = detector.detectAndDecode(img_cv)

            if qr_content:
                qr_content = qr_content.strip()

                # Split QR data
                if '|' not in qr_content:
                    result = "Scan Failed: Invalid QR format"
                else:
                    qr_data, qr_mobile_number = qr_content.rsplit('|', 1)

                    qr_entry = QRcode.objects.filter(
                        data=qr_data,
                        mobile_number=qr_mobile_number
                    ).first()

                    if qr_entry and qr_mobile_number == mobile_number:
                        result = "Scan Success: Valid QR Code for the provided mobile number"

                        # Delete database entry
                        qr_entry.delete()

                        # Delete generated QR image
                        safe_data = slugify(qr_data)[:50] or 'qr'
                        generated_qr_path = (
                            Path(settings.MEDIA_ROOT)
                            / 'qr_codes'
                            / f"{safe_data}_{qr_mobile_number}.png"
                        )

                        if generated_qr_path.exists():
                            generated_qr_path.unlink()
                    else:
                        result = "Scan Failed: Invalid QR code or mobile number mismatched"
            else:
                result = "No QR code detected in the image"

        except Exception as e:
            result = f"Error processing image: {str(e)}"

        finally:
            # Delete uploaded image
            if qr_image_path and qr_image_path.exists():
                qr_image_path.unlink()

    return render(request, 'scanner/scan.html', {
        'result': result
    })