## Dicoding Collection Dashboard ✨

### Setup Environment - Shell/Terminal
1. Pastikan Anda memiliki folder bernama `finpro dicoding`.
2. Masuk ke folder tersebut melalui terminal:
`cd finpro dicoding`
3. Buat dan aktifkan virtual environment:
`pipenv install pipenv shell`
4. install semua package yang diperlukan:
`pip install -r requirements.txt`

#### Tidak perlu bernama `finpro dicoding` --> contoh = `submission`, cukup pastikan strukturnya
```
(env) submission
      ├───dashboard
      | ├───main_data.csv
      | ├───day_cleaned.csv
      | └───dashboard.py
      | ├───bike_rent_logo.png
      ├───data
      | ├───day.csv
      | └───hour.csv
      ├───notebook.ipynb
      ├───README.md
      └───requirements.txt
      └───URL.txt
```

### Run streamlit app
```
streamlit run dashboard/dashboard.py
```

Setelah menjalankan perintah di atas, sebuah link akan muncul di terminal, seperti berikut:

   ```
   Local URL: http://localhost:8501
   Network URL: http://<your_ip>:8501
   ```
