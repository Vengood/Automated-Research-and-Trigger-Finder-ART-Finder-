require('dotenv').config();
const express=require('express');
const app=express();
const client=require('./config/db')
const AuthRouter=require('./routes/AuthRouter');
const cors=require('cors')

app.use(express({extends : true}));
app.use(express.json());

app.get('/',(req,res)=>{
    res.status(200).json({msg : "Welcome to server"});
})
app.use(cors())
app.use('/auth',AuthRouter);




app.listen(process.env.PORT,()=>{
    console.log(`Server running on port : ${process.env.PORT}`);
})