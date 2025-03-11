# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Validasi input data

def validate_nik(nik):
    """Memvalidasi NIK (harus 16 digit angka)."""
    return bool(re.fullmatch(r"\d{16}", nik))

def validate_name(name):
    """Memvalidasi nama (hanya huruf dan spasi, minimal 2 karakter)."""
    return bool(re.fullmatch(r"[A-Za-z ]{2,}", name))

def validate_date(date):
    """Memvalidasi format tanggal (YYYY-MM-DD)."""
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date))

def validate_payment(amount):
    """Memvalidasi jumlah pembayaran (hanya angka dan minimal 1)."""
    return bool(re.fullmatch(r"\d+", str(amount)))
