# Youbify 🎵➡️🎥   
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) ![Tailwdincss](https://img.shields.io/badge/tailwindcss-0F172A?&logo=tailwindcss)  ![SpotifyAPI](https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white) ![GoogleAPIs](https://img.shields.io/badge/Google_APIs-4285F4?style=for-the-badge&logo=google&logoColor=white) ![Youtube](https://img.shields.io/badge/Youtube-FF0000?logo=youtubemusic)

**Youbify** is a web application that allows users to seamlessly transfer their Spotify playlists to YouTube (Music). The app provides a simple and efficient way to migrate playlists without manually searching for each song.



![error image](https://github.com/AlexandruCrisan/Youbify/blob/master/brosura_res/Home.PNG?raw=true) 
---

## 🌟 Features

- 🔑 **Login with Spotify and Google** to access your playlists.
- 📜 **Select specific playlists** from Spotify to transfer.
- 🚀 **Automatic song matching** to YouTube (Music).
- 🎵 **Seamless integration** with Spotify API & YouTube API.
- 🎨 **Simple UI** using Tailwind CSS.

---

## 🛠️ Tech Stack
- **Backend:** Django (Python) - API & template engine
- **Frontend:** Django templates + Tailwind CSS
- **Authentication:** Spotify OAuth & Google OAuth
- **APIs Used:** Spotify Web API, YouTube Data API

---

## [🎬 Demo Video](https://youtu.be/n4KFS1eEcwo)



Click the link above to watch Youbify in action!

---

## 🔑 Authentication Flow

### **Spotify OAuth Flow**

Below is the authentication flow for Spotify login:
![error image](https://github.com/AlexandruCrisan/Youbify/blob/master/brosura_res/auth-code-flow-spotify.png?raw=true)


### **Google OAuth Flow**

Youbify uses Google APIs to authenticate YouTube Music access, following Google's standard OAuth process.

---

## 🚀 Getting Started

### **1️⃣ Clone the Repository**

```sh
 git clone https://github.com/AlexandruCrisan/Youbify.git
 cd Youbify
```

### **2️⃣ Install Dependencies**

```sh
 pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**

Create a `.env` file and add:

```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=redirect_uri (usually /api/spotify/redirect)
YOUTUBE_REDIRECT_URI=redirect_uri (usually /api/youtube/redirect)
```
### **3️⃣.1️⃣ (Optional) Database related variables**

```env
DB_ENGINE=your_engine
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_pw
DB_HOST=database_host
DB_PORT=database_port
```


### **4️⃣ Run the Server**

```sh
 python manage.py runserver
```

---

## 📜 License

This project is licensed under the MIT License.

---

> Made by [Crisan Alexandru](https://github.com/AlexandruCrisan)

