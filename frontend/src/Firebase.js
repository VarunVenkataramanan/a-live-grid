// Replace with your Firebase config
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
    apiKey: "AIzaSyA3Q91RKuwJcp_gfD0HuN9GMTLh-UN9teE",
    authDomain: "a-livegrid.firebaseapp.com",
    projectId: "a-livegrid",
    storageBucket: "a-livegrid.firebasestorage.app",
    messagingSenderId: "869205359468",
    appId: "1:869205359468:web:4385b64705fd7958fc1149",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
