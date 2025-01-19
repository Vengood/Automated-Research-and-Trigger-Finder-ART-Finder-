import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";
const Login = () => {
    const [email,setEmail]=useState('');
    const [password,setPassword]=useState('');
    const navigate=useNavigate();

    
      
    
    

    const handleSubmit = async (e) => {
      e.preventDefault();
      
    
      if (!email || !password) {
        alert("Please fill in all the fields.");
        return;
      }
    
      try {
        const response = await axios.post("http://localhost:8080/auth/login", {
          email,
          password,
        });
    
        if (response.data.success) {
          alert(response.data.msg); // Show success message
          // Optionally store the JWT token in localStorage or cookies
          localStorage.setItem("token", response.data.jwToken);
          // Redirect user to the dashboard or another page
          navigate('/home')
        } else {
          alert(response.data.msg || "Login failed. Please try again.");
        }
      } catch (err) {
        console.error("Error during login:", err);
        const errorMessage = err.response?.data?.msg || "An error occurred. Please try again.";
        alert(errorMessage);
      }
    };
    
    
      return (
       <div className='h-screen w-screen bg-black flex items-center justify-center gap-9'>
        <div className='w-[60%] rounded-md p-3 h-screen flex flex-col justify-center '>
           <video src="https://videos.pexels.com/video-files/25744121/11904044_640_360_25fps.mp4" autoPlay muted loop className='object-fill rounded-lg'></video>
        </div>
        <div className='w-1/2 flex justify-center '>
        <div className='w-1/2 flex flex-col  rounded-md gap-5  '>
            <div className='p-4 flex flex-col gap-3'>
            <h1 className='text-white  font-semibold text-2xl font-Gilroy '>Login</h1>
            <p className=' text-sm text-gray-300 font-Gilroy'>Welcome to  ART Finder.Login With Your Creditionals</p>
            </div>
            <form className='flex flex-col p-5 py-3  gap-6  ' >

                <input type="text"
                className='px-3 py-2 bg-transparent  rounded-lg outline-none  border-[0.2px] border-gray-400 text-white ' 
                placeholder="email"
                value={email}
                onChange={(e)=>setEmail(e.target.value)}
                /><input type="text" 
                className='px-3 py-2 bg-transparent  rounded-lg outline-none  border-[0.2px] border-gray-400 text-white '
                placeholder='password'
                value={password}
                onChange={(e)=>setPassword(e.target.value)}
                
                />

                <button 
                className='px-3 py-2 bg-white text-black rounded-lg font-bold'
                onClick={handleSubmit}
                >
                    Login
                </button>
                <p className='text-white '>Dont Have An Account? <Link to='/signup'>SignUP</Link> </p>
            </form>
            
        </div>
        </div>
       </div>
      );
}

export default Login