# Firebase & Google Cloud Storage Setup Guide

## 🚀 **Complete Firebase Integration for A-Live-Grid**

Your backend now supports:
- ✅ **Firebase Authentication** (Google OAuth)
- ✅ **Firestore Database** (NoSQL)
- ✅ **Google Cloud Storage** (Image uploads)
- ✅ **Real-time data** (Firestore)

## 📋 **Setup Steps**

### **1. Firebase Project Setup**

You already have your Firebase project: `a-livegrid`

### **2. Service Account Setup**

#### **Step A: Create Service Account**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `a-livegrid`
3. Go to **Project Settings** → **Service Accounts**
4. Click **"Generate new private key"**
5. Download the JSON file

#### **Step B: Configure Backend**
1. Place the downloaded JSON file in your backend directory
2. Update your `.env` file:

```env
# Firebase Configuration
GOOGLE_APPLICATION_CREDENTIALS=./path/to/your/service-account-key.json
FIREBASE_PROJECT_ID=a-livegrid
FIREBASE_API_KEY=AIzaSyA3Q91RKuwJcp_gfD0HuN9GMTLh-UN9teE
FIREBASE_AUTH_DOMAIN=a-livegrid.firebaseapp.com
FIREBASE_STORAGE_BUCKET=a-livegrid.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=869205359468
FIREBASE_APP_ID=1:869205359468:web:4385b64705fd7958fc1149

# Security
SECRET_KEY=your-super-secret-key-here
```

### **3. Install Dependencies**

```bash
cd a-live-grid/backend
pip install -r requirements.txt
```

### **4. Enable Firebase Services**

#### **A. Authentication**
1. Go to **Authentication** → **Sign-in method**
2. Enable **Google** provider
3. Add your domain to authorized domains

#### **B. Firestore Database**
1. Go to **Firestore Database**
2. Click **"Create database"**
3. Choose **"Start in test mode"** (for development)
4. Select a location (choose closest to your users)

#### **C. Storage**
1. Go to **Storage**
2. Click **"Get started"**
3. Choose **"Start in test mode"** (for development)
4. Select a location

## 🔐 **Frontend Integration**

### **Frontend Authentication Flow**

```javascript
// Your existing Firebase config
const firebaseConfig = {
    apiKey: "AIzaSyA3Q91RKuwJcp_gfD0HuN9GMTLh-UN9teE",
    authDomain: "a-livegrid.firebaseapp.com",
    projectId: "a-livegrid",
    storageBucket: "a-livegrid.firebasestorage.app",
    messagingSenderId: "869205359468",
    appId: "1:869205359468:web:4385b64705fd7958fc1149",
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Google Sign-in
async function signInWithGoogle() {
    const provider = new firebase.auth.GoogleAuthProvider();
    try {
        const result = await firebase.auth().signInWithPopup(provider);
        const user = result.user;
        const token = await user.getIdToken();
        
        // Store token for API calls
        localStorage.setItem('firebase_token', token);
        
        return user;
    } catch (error) {
        console.error('Sign-in error:', error);
    }
}

// Get current user token
async function getAuthToken() {
    const user = firebase.auth().currentUser;
    if (user) {
        return await user.getIdToken();
    }
    return null;
}
```

### **API Calls with Authentication**

```javascript
// Example: Upload post with image
async function uploadPostWithImage(formData) {
    const token = await getAuthToken();
    
    const response = await fetch('http://localhost:8000/api/v1/posts/upload-with-image', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });
    
    return await response.json();
}

// Example: Get posts
async function getPosts() {
    const response = await fetch('http://localhost:8000/api/v1/posts/short');
    return await response.json();
}
```

## 📱 **Mobile App Integration**

### **Android (Kotlin)**

```kotlin
// Add Firebase dependencies to build.gradle
implementation 'com.google.firebase:firebase-auth:22.1.2'
implementation 'com.google.firebase:firebase-firestore:24.8.1'
implementation 'com.google.firebase:firebase-storage:20.2.1'

// Google Sign-in
private fun signInWithGoogle() {
    val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
        .requestIdToken("your-web-client-id")
        .requestEmail()
        .build()
    
    val googleSignInClient = GoogleSignIn.getClient(this, gso)
    val signInIntent = googleSignInClient.signInIntent
    startActivityForResult(signInIntent, RC_SIGN_IN)
}

// Get Firebase token
private fun getFirebaseToken(onSuccess: (String) -> Unit) {
    FirebaseAuth.getInstance().currentUser?.getIdToken(true)
        ?.addOnCompleteListener { task ->
            if (task.isSuccessful) {
                val token = task.result?.token
                token?.let { onSuccess(it) }
            }
        }
}

// Upload post
private fun uploadPost(title: String, imageUri: Uri) {
    getFirebaseToken { token ->
        // Upload to your backend
        val formData = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("title", title)
            .addFormDataPart("image", imageUri.toString())
            .build()
        
        val request = Request.Builder()
            .url("http://localhost:8000/api/v1/posts/upload-with-image")
            .addHeader("Authorization", "Bearer $token")
            .post(formData)
            .build()
        
        // Execute request...
    }
}
```

### **iOS (Swift)**

```swift
// Add Firebase dependencies via CocoaPods
// pod 'Firebase/Auth'
// pod 'Firebase/Firestore'
// pod 'Firebase/Storage'

import Firebase
import GoogleSignIn

// Configure Firebase
FirebaseApp.configure()

// Google Sign-in
func signInWithGoogle() {
    guard let clientID = FirebaseApp.app()?.options.clientID else { return }
    
    let config = GIDConfiguration(clientID: clientID)
    GIDSignIn.sharedInstance.configuration = config
    
    GIDSignIn.sharedInstance.signIn(withPresenting: self) { result, error in
        guard let user = result?.user,
              let idToken = user.idToken?.tokenString else { return }
        
        let credential = GoogleAuthProvider.credential(withIDToken: idToken,
                                                     accessToken: user.accessToken.tokenString)
        
        Auth.auth().signIn(with: credential) { result, error in
            // Handle sign-in result
        }
    }
}

// Get Firebase token
func getFirebaseToken(completion: @escaping (String?) -> Void) {
    Auth.auth().currentUser?.getIDToken { token, error in
        completion(token)
    }
}

// Upload post
func uploadPost(title: String, image: UIImage) {
    getFirebaseToken { token in
        guard let token = token else { return }
        
        // Convert image to data
        guard let imageData = image.jpegData(compressionQuality: 0.8) else { return }
        
        // Create form data
        let boundary = UUID().uuidString
        var request = URLRequest(url: URL(string: "http://localhost:8000/api/v1/posts/upload-with-image")!)
        request.httpMethod = "POST"
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        // Build multipart form data...
        // Send request...
    }
}
```

## 🔧 **Backend API Endpoints**

### **Authentication Required Endpoints**
- `POST /api/v1/posts/` - Create post
- `POST /api/v1/posts/upload-with-image` - Upload post with image
- `POST /api/v1/posts/upload-bitmap` - Upload post with bitmap
- `POST /api/v1/posts/{post_id}/vote` - Vote on post
- `DELETE /api/v1/posts/{post_id}` - Delete post
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update user profile

### **Public Endpoints**
- `GET /api/v1/posts/short` - Get feed
- `GET /api/v1/posts/long` - Get detailed posts
- `GET /api/v1/posts/{post_id}` - Get specific post

## 🚀 **Running the Backend**

```bash
cd a-live-grid/backend
python run.py
```

Your API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 **Security Rules**

### **Firestore Security Rules**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Posts can be read by anyone, written by authenticated users
    match /posts/{postId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Votes can be read/written by authenticated users
    match /votes/{voteId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### **Storage Security Rules**
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Allow authenticated users to upload images
    match /posts/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

## 🎯 **Next Steps**

1. **Test Authentication**: Try signing in with Google
2. **Upload Images**: Test image upload functionality
3. **Create Posts**: Test post creation with images
4. **Real-time Updates**: Implement real-time feed updates
5. **Production Deployment**: Deploy to production environment

Your backend is now fully integrated with Firebase! 🎉 