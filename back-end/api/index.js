const express = require('express');
const mongoose = require('mongoose');
const User = require('./models/User');
const bycrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const app = express();

const salt = bycrypt.genSaltSync(10);
const secret = bycrypt.genSaltSync(10);

app.use(cors({credentials: true, origin: 'http://localhost:3000'}));
app.use(express.json());

mongoose.connect('mongodb+srv://timothyarinze:timothy@yourhr.byb2dk6.mongodb.net/?retryWrites=true&w=majority');
app.post('/register', async (req, res) => {
    try {
        const {firstName, lastName, emailAddress, employeeID, DOB, department, password} = req.body;
        const userDoc = await User.create({firstName, lastName, emailAddress, employeeID, DOB, department, 
            password: bycrypt.hashSync(password, salt)});
        res.json(userDoc);
    } catch (error) {
        console.log(error);
        res.status(400).json({errorMessage: 'Please try again later'});
    }
});

app.post('/login', async (req, res) => {
    const {emailAddress, password} = req.body;
    const userDoc = await User.findOne({emailAddress});
    const passOk = bycrypt.compareSync(password, userDoc.password);
    if (passOk) {
        jwt.sign({emailAddress}, secret, {expiresIn: 3600}, (err, token) => {
            if (err) {
                res.status(400).json({errorMessage: 'Please try again later'});
            } else {
                res.cookie('token', token, {httpOnly: true}).json({message: 'Login successful'});
            }})
        } else {
                res.status(400).json({errorMessage: 'Please try again later'});
            }
});


app.listen(4000);