# Bai 7.3 - GitHub Actions

## Dung khi nao

- Khi submit local/Colab/VPN van chi duoc `4/5`.
- Khi nghi he thong cham theo IP/context cua may gui.

## Cach dung nhanh

1. Tao mot repo GitHub moi.
2. Upload toan bo thu muc bai nay len repo.
3. Vao tab `Actions`.
4. Chon workflow `Submit Bai 7.3`.
5. Bam `Run workflow`.
6. Mo log buoc `Submit and verify bai 7.3`.

## File quan trong

- `submission-shot-dallas-exact.png`: anh nop bai
- `submit-bai73.py`: script submit + verify
- `.github/workflows/submit-bai73.yml`: workflow GitHub Actions

## Ket qua can nhin

- `Runner IP / Geo`: xem runner dang o dau
- `Ket qua submit`: submit co thanh cong hay khong
- `Ket qua verify lan X`: check co len `valid: true` hay khong

## Neu van 4/5

- Runner GitHub Actions do khong ra US theo cach server cham
- Hoac bai nay dung metadata/session khac nua
- Luc do dung VPS US that la duong gon nhat
