
---

````markdown

🔎 SecretScanner

---

## 📘 Açıklama

**SecretScanner**, web sitelerini tarayarak JavaScript, HTML veya diğer kaynaklarda **gizli anahtarları**  
(API key, token, secret vb.) tespit etmek için geliştirilmiş bir güvenlik aracıdır.

> 🔁 Araç, **Depth 3** seviyesine kadar bağlantıları takip eder ve `dir`, `sub`, `all` modlarını destekler.  
> ⚡ Multi-threaded çalışır, proxy desteği vardır, duplicate sonuçları temizler ve cross-endpoint doğrulaması yapar.  
> 📊 Sonuçları JSON formatında kaydeder ve **Aquatone tarzı HTML rapor** üretir.

---

## ⚙️ Özellikler

- 🧩 **Anahtar Tespiti:** `api_key`, `secret`, `token`, `access_key`, `client_secret`, `private_key`, `jwt`, `password`, `pem`, `rsa`, `ssh`, `auth`, `Auth`, `Key`, `PwD`
- 🔁 **Çapraz Endpoint Doğrulaması:** Bulunan key’lerin hedef URL üzerinde aktif olup olmadığını test eder.
- ⚡ **Multi-threaded Tarama:** Çoklu iş parçacığı ile hızlı analiz.
- 🌐 **Depth 3 Link Tarama:** Maksimum 3 seviye derinliğe kadar linkleri takip eder.
- 📊 **JSON ve HTML Raporlama:** JSON ve görsel HTML rapor üretir.
- 🧱 **Proxy Desteği:** Trafiği özel proxy üzerinden yönlendirme imkânı.

---

## 🧰 Kullanım

### 🔹 Tek URL Tarama
```bash
python3 spider.py -u https://hedefsite.com -m dep1 -m dep2 -m dep3 -m dir -th 50
````

### 🔹 URL Listesi Tarama

```bash
python3 spider.py -t urls.txt -m all -th 30
```

### 🔹 Proxy Kullanarak Tarama

```bash
python3 spider.py -u https://hedefsite.com -m all --proxy http://127.0.0.1:8080
```

---

## 📂 Çıktılar

| Dosya                          | Açıklama                                             |
| ------------------------------ | ---------------------------------------------------- |
| **urls.txt**                   | Tarama sırasında keşfedilen tüm URL’ler              |
| **raw_findings.json**          | Ham tespit edilen key’ler ve cURL komutları          |
| **tested_findings.json**       | Cross-endpoint doğrulama sonucu test edilmiş key’ler |
| **aquatone_style_report.html** | Görsel HTML rapor                                    |

---

## ⚠️ Uyarı

> Bu araç yalnızca **yetkili test ortamlarında** kullanılmalıdır.
> İzinsiz testler **yasal sorumluluk doğurur** ve kullanıcıya aittir.

---

## 🧑‍💻 Geliştirici

| İsim          | Rol                                  |
| ------------- | ------------------------------------ |
| **0bat.exe1** | Geliştirici / Güvenlik Araştırmacısı |

---

## 📜 Lisans

Bu proje **MIT Lisansı** altında yayınlanmıştır.
Dilediğin gibi kullanabilir, düzenleyebilir ve paylaşabilirsin.

---




