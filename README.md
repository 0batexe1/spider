Açıklama
--------
Bu araç, web sitelerini tarayarak JavaScript, HTML veya diğer kaynaklarda gizli anahtarları (API key, token, secret vb.) tespit etmek için geliştirilmiştir.

Depth 3’e kadar linkleri takip eder (dep1, dep2, dep3)

dir, sub, all modlarını destekler

Multi-threaded çalışır ve proxy desteği vardır

Duplicate sonuçları temizler ve cross-endpoint doğrulaması yapar

JSON çıktısı üretir ve Aquatone tarzı HTML rapor oluşturur

Özellikler
----------

Anahtar tespiti: api_key, secret, token, access_key, client_secret, private_key, jwt, password, pem, rsa, ssh, auth, Auth, Key, PwD

Çapraz endpoint doğrulaması: Bulunan key’lerin hedef URL üzerinde aktif olup olmadığını test eder

Multi-threaded tarama: Birden fazla iş parçacığı ile hızlı tarama

Depth 3 link tarama: Maksimum 3. seviyeye kadar linkleri takip eder

JSON ve HTML rapor: Test edilen key’leri JSON dosyası olarak kaydeder ve görsel HTML rapor üretir

Kullanım
---------
Tek URL tarama
python3 spider.py -u https://hedefsite.com -m dep1 -m dep2 -m dep3 -m dir -th 50

URL listesi tarama
python3 spider.py -t urls.txt -m all -th 30

Proxy kullanarak tarama
python3 spider.py -u https://hedefsite.com -m all --proxy http://127.0.0.1:8080

Çıktılar

urls.txt → Tarama sırasında keşfedilen tüm URL’ler

raw_findings.json → Ham tespit edilen key’ler ve cURL komutları

tested_findings.json → Cross-endpoint doğrulama sonucu key’ler

aquatone_style_report.html → Görsel HTML rapor

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Description
-----------
This tool is designed to scan websites and detect sensitive keys (API keys, tokens, secrets, etc.) in JavaScript, HTML, or other sources.

Follows links up to depth 3 (dep1, dep2, dep3)

Supports dir, sub, and all modes

Multi-threaded with optional proxy support

Removes duplicates and performs cross-endpoint validation

Outputs JSON results and generates an Aquatone-style HTML report

Features
--------
Key detection: api_key, secret, token, access_key, client_secret, private_key, jwt, password, pem, rsa, ssh, auth, Auth, Key, PwD

Cross-endpoint validation: Tests whether detected keys are active on target URLs

Multi-threaded scanning: Fast scanning with multiple threads

Depth 3 link crawling: Follows links up to 3 levels deep

JSON & HTML report: Saves scanned keys in JSON and generates visual HTML report

Usage
-----
Scan a single URL
python3 spider.py -u https://targetsite.com -m dep1 -m dep2 -m dep3 -m dir -th 50

Scan a list of URLs
python3 spider.py -t urls.txt -m all -th 30

Scan using a proxy
python3 spider.py -u https://targetsite.com -m all --proxy http://127.0.0.1:8080

Outputs
-------
urls.txt → All discovered URLs during scanning

raw_findings.json → Raw detected keys and corresponding cURL commands

tested_findings.json → Keys verified via cross-endpoint testing

aquatone_style_report.html → Visual HTML report
