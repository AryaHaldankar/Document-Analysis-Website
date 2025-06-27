// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, onAuthStateChanged, signOut } from "firebase/auth";
import {createAuthUI} from "./ui.js";
import './styles.css';

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCs0HIphCmN8K2DW8ArintWsFtp2wILIFg",
  authDomain: "docanpr-890f4.firebaseapp.com",
  projectId: "docanpr-890f4",
  storageBucket: "docanpr-890f4.firebasestorage.app",
  messagingSenderId: "36419654145",
  appId: "1:36419654145:web:81d76164be55cfcb912600"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app)

const verifyUser = async (userCredential) => {
  try {
    // Get the Firebase ID token
    const idToken = await userCredential.user.getIdToken();

    // Send the token to your backend
    const response = await fetch("http://localhost:8080/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ usr_id: idToken }), // Match expected Go struct field
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Server error");
    }

    console.log("✅ Backend login success:", data);
    return data;
  } catch (error) {
    console.error("❌ verifyUser error:", error);
    return { success: false, error: error.message };
  }
};


const loginEmailPassword = async (loginEmail, loginPassword) => {
  const userCredential = await signInWithEmailAndPassword(auth, loginEmail, loginPassword);
  console.log(userCredential.user);
  const verification = await verifyUser(userCredential);
}
const signupEmailPassword = async (signupEmail, signupPassword) => {
  const userCredential = await createUserWithEmailAndPassword(auth, signupEmail, signupPassword);
  console.log(userCredential.user);
  const verification = await verifyUser(userCredential);
}
const logOut = async () =>{
  await signOut(auth);
}
const appDiv = document.getElementById('app');
const logOutButton = document.createElement('button');
logOutButton.textContent = 'Log Out';
logOutButton.addEventListener('click', () => {
  logOut();
});
const monitorAuthChanged = async () => {
  onAuthStateChanged(auth, (user) =>{
    if (user){
      if (!appDiv.contains(logOutButton)) {
        appDiv.appendChild(logOutButton);
      }
    }
    else{
      if (appDiv.contains(logOutButton)) {
        appDiv.removeChild(logOutButton);
      }
    }
  })
}
appDiv.appendChild(createAuthUI(signupEmailPassword, loginEmailPassword));
monitorAuthChanged();