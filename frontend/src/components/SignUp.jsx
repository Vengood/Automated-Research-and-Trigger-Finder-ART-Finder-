import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';

import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import axios from "axios";
const SignUp = () => {
  const[name,setName]=useState('')
  const[email,setEmail]=useState('')
  const[password,setPassword]=useState('')
  const navigate=useNavigate();
  



const handleSubmit = async (e) => {
  e.preventDefault();
  

  if (!name || !email || !password) {
    alert("Please fill in all the fields.");
    return;
  }

  try {
    const response = await axios.post("http://localhost:8080/auth/signup", {
      name,
      email,
      password,
    });

    if (response.data.success) {
      alert(response.data.msg); // Show success message
      // Optionally, redirect to the login page
      navigate('/login')
    } else {
      alert(response.data.msg || "Signup failed. Please try again.");
    }
  } catch (err) {
    console.error("Error during signup:", err);
    const errorMessage = err.response?.data?.msg || "An error occurred. Please try again.";
    alert(errorMessage);
  }
};


  return (
    <div className="h-screen w-screen bg-black flex items-center justify-center gap-9">
      <div className="w-[60%] rounded-md p-3 h-screen flex flex-col justify-center ">
        <video
          src="https://videos.pexels.com/video-files/25744121/11904044_640_360_25fps.mp4"
          autoPlay
          loop
          muted
          className="object-fill rounded-lg"
        ></video>
      </div>
      <div className="w-1/2 flex justify-center ">
        <div className="w-1/2 flex flex-col  rounded-md gap-5  ">
          <div className="p-4 flex flex-col gap-3">
            <h1 className="text-white  font-semibold text-2xl font-Gilroy ">
              SignUP
            </h1>
            <p className=" text-sm text-gray-300 font-Gilroy">
              Welcome to ART Finder.Create Your Account 
            </p>
          </div>
          <form className="flex flex-col p-2 py-3  gap-6  ">
            <input
              type="text"
              className="px-3 py-2 bg-transparent  rounded-lg outline-none  border-[0.2px] border-gray-400 text-white "
              placeholder="Name"
              value={name}
              onChange={(e)=>setName(e.target.value)}
            />

            <input
              type="text"
              className="px-3 py-2 bg-transparent  rounded-lg outline-none  border-[0.2px] border-gray-400 text-white "
              placeholder="email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
            />
            <input
              type="text"
              className="px-3 py-2 bg-transparent  rounded-lg outline-none  border-[0.2px] border-gray-400 text-white "
              placeholder="password"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
            />
            {/* <input
              type="text"
              className="px-3 py-2 bg-transparent  rounded-lg outline-none  border-[0.2px] border-gray-400 text-white "
              placeholder="confirm passoward"
            /> */}

            <button onClick={handleSubmit} className="px-3 py-2 bg-white text-black rounded-lg font-bold">
              SignUp
            </button>
          </form>
          <p>Already Have An Account <Link to='/login'>Login</Link> </p>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
