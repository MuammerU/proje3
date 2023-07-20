import streamlit as st
import pandas as pd
import numpy as np
import joblib
st.set_page_config(
    page_title="Diabets Test",
    page_icon="https://static.vecteezy.com/system/resources/previews/011/420/406/original/world-diabetes-day-elements-png.png", 
    menu_items={
        "Get help": "mailto:muammerugur@gmail.com",
        "About": "Bu web sitesi, verilerinizi kullanarak size diyabet olma olasılığınız hakkında bir tahminde bulunmak amacıyla oluşturulmuştur. Lütfen sonuçları kesin bir teşhis yerine almayın ve sağlık durumunuzu belirlemek için doktorunuza danışın." + "Daha fazla bilgi için\n" + "muammerugur@gmail.com"
    }
)

# Başlık Ekleme
st.title("Diyabet Testi")

#Markdown oluşturma
st.markdown("Merhaba! Bu web sitesi, diyabet olup olmadığınıza dair tahminde bulunmak için kullanılabilir. Lütfen yanda bulunan formu doldurarak bilgilerinizi girin, böylece size tahmin sonucunuzu gösterebiliriz.")

# Resim Ekleme
st.image("https://www.med-technews.com/downloads/4867/download/diabetes.png?cb=20ae2efb77d63abfd2808a089c2d911c&w=1000")

# Header Ekleme
st.header("Kullandığımız verileri kısaca açıklamak gerekirse:")

st.markdown("- **gender**: Cinsiyet Bilgisi")
st.markdown("- **age**: Bireyin yaşı")
st.markdown("- **hypertension**: Hipertansiyonan sahip olup olmadığı bilgisi (0 = Hipetansiyona sahip değil 1 = Hipertansiyona sahip)")
st.markdown("- **heart_disease**: Bir kalp rahatsızlığının olup olmadığı bilgisi  (0 = Sahip değil 1 = Sahip) ")
st.markdown("- **ysmoking_history**: Sigara kullanım alışkanlığı")
st.markdown("- **bmi**: Vücut Kitle Endeksi (Vücut ağırlığınız/boyunuzun karesi)")
st.markdown("- **hba1c_level**: HbA1c (Hemoglobin A1c) seviyesi, bir kişinin son 2-3 aydaki ortalama kan şekeri seviyesinin bir ölçüsüdür.")
st.markdown("- **blood_glucose_level**: Kan şekeri seviyesi, belirli bir zamanda kan dolaşımındaki glikoz miktarını")


st.sidebar.markdown("**Test Sonucunu GÖrmek İçin Formu Eksiksiz Şekilde Doldurun!**")

# Sidebarda Kullanıcıdan Girdileri Alma
Ad = st.sidebar.text_input("Ad")
Soyad = st.sidebar.text_input("Soyad")
Yaş = st.sidebar.number_input("Yaş", min_value=0,max_value=100)
BMİ = st.sidebar.number_input("Vücut Kitle Endeksi", min_value=10.0,max_value=100.0,help="Vücut kitle endeksinizi bilmiyorsanız bu link üzerinden öğrenebilirsiniz: https://www.calculator.net/bmi-calculator.html")
HbA1c = st.sidebar.number_input("HbA1c Seviyesi", min_value=3.5,max_value=9.0,help="Bu değer yapılan testlerin sonucundan elde edilir 3.5-9 arasında yer alır")
Kan_şekeri_seviyesi = st.sidebar.slider("Kan Şekeri Seviyesi", min_value=80, max_value=300,help="Bu değer yapılan testlerin sonucundan elde edilir 80-300 arasında yer alır")

# Pickle kütüphanesi kullanarak eğitilen modelin tekrardan kullanılması
import joblib
from joblib import load

web_model = joblib.load("web_model.pkl")



#from sklearn.preprocessing import OneHotEncoder
#input_df = pd.get_dummies(input_df, columns = ["age"], prefix = ["age"],drop_first= True)


#input_df = pd.get_dummies(input_df, columns = ["bmi"], prefix = ["bmi"],drop_first= True)




#input_df = pd.get_dummies(input_df, columns = ["hba1c_level"], prefix = ["hba1c_level"],drop_first= True)



#input_df = pd.get_dummies(input_df, columns = ["blood_glucose_level"], prefix = ["blood_glucose_level"],drop_first= True)


#pred = model_xgboost_diabetes_model.predict(input_df.values)

#import pickle

# Load the trained XGBoost model from the pkl file
#with open("model_xgboost_diabetes.pkl", "rb") as f:
    #model_xgboost_diabetes_model = pickle.load(f)

input_df = pd.DataFrame({
    'age': [Yaş],
    'bmi': [BMİ],
    'hba1c_level': [HbA1c],
    'blood_glucose_level': [Kan_şekeri_seviyesi]
})    

# Now you can use the loaded model for predictions
pred = web_model.predict(input_df)
pred_probability = np.round(web_model.predict_proba(input_df), 2)

st.header("**Sonuç**")

# Sonuç Ekranı
if st.sidebar.button("Gönder"):

    # Info mesajı oluşturma
    st.info("Sonucunuzu aşağıda görebilirsiniz.")

    # Sorgulama zamanına ilişkin bilgileri elde etme
    from datetime import date, datetime

    today = date.today()
    time = datetime.now().strftime("%H:%M:%S")

    # Sonuçları Görüntülemek için DataFrame
    results_df = pd.DataFrame({
    
    'Tarih': [today],
    'Saat': [time],
    'Ad': [Ad],
    'Soyad': [Soyad],
    'Yaş': [Yaş],
    'Vücut Kitle Endeksi': [BMİ],
    'HbA1c Seviyesi': [HbA1c],
    'Kan_şekeri_seviyesi': [Kan_şekeri_seviyesi],
    'Prediction': [pred],
    'Diyabet Olmama Olasılığınız': [pred_probability[:,:1]],
    'Diyabet Olma Olasılığınız': [pred_probability[:,1:]]
    })
    results_df['Diyabet Olmama Olasılığınız'] = results_df['Diyabet Olmama Olasılığınız'].astype(float)
    results_df['Diyabet Olma Olasılığınız'] = results_df['Diyabet Olma Olasılığınız'].astype(float)

    results_df["Prediction"] = results_df["Prediction"].apply(lambda x: str(x).replace("0","Diyabet Değil"))
    results_df["Prediction"] = results_df["Prediction"].apply(lambda x: str(x).replace("1","Diyabet"))

    st.table(results_df)








