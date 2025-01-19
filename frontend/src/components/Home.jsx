import React, { useState } from 'react';
import { Search, Sparkles, Tag, Gamepad2 } from 'lucide-react';

function Home() {
  const [query, setQuery] = useState('');
  const [keywords, setKeywords] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = (e) => {
    
  };

  

  return (
    <div className='h-screen w-full bg-black flex justify-center items-center'>
        <div className='w-[80%]'>
            <form  className='flex flex-col gap-6 w-full'>
                <input type="text"
                placeholder='Enter Your Query'
                value={query}
                onChange={(e)=>setQuery(e.target.value)}
                className='text-white placeholder:text-lg text-xl px-4 py-4 bg-gray-500 rounded-lg outline-none'
                />
                <input type="text"
                placeholder='Enter Your keywords , separated'
                value={keywords} 
                onChange={(e)=>setKeywords(e.target.value)}
                className='text-white placeholder:text-lg text-xl px-4 py-4 bg-gray-500 rounded-lg outline-none'
                />

                <button className='bg-white py-3 text-black font-bold rounded-lg'>
                    Search Your Query
                </button>
            </form>
        </div>
    </div>
  );
}

export default Home;
