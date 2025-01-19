import { useState } from 'react'
import Login from './components/Login'
import SignUp from './components/SignUp'
import Home from './components/Home'
import Results from './components/Results'
import { Route, Routes } from "react-router-dom";


import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='w-full'>
     <Routes>
        <Route path='/' element={<Login/>}></Route>
        <Route path='/login' element={<Login/>}></Route>
        <Route path='/signup'  element={<SignUp/>}></Route>
        <Route path='/home' element={<Home/>}></Route>
        <Route path='/results' element={<Results/>}></Route>
     </Routes>
    </div>
  )
}

export default App
