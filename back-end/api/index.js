const express = require('express');
const mongoose = require('mongoose');
const User = require('./models/User');
const bycrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const app = express();
const cookieParser = require('cookie-parser');

const salt = bycrypt.genSaltSync(10);
const secret = bycrypt.genSaltSync(10);

app.use(cors({credentials: true, origin: 'http://localhost:3000'}));
app.use(express.json());
app.use(cookieParser());

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
        jwt.sign({emailAddress, id:userDoc._id}, secret, {expiresIn: 3600}, (err, token) => {
            if (err) throw err;
            res.cookie('token', token).json({
                id: userDoc._id,
                firstName: userDoc.firstName,
                lastName: userDoc.lastName,
                emailAddress: userDoc.emailAddress,
                employeeID: userDoc.employeeID,
                DOB: userDoc.DOB,
                department: userDoc.department,
                AnnualLeave: userDoc.AnnualLeave,
                SickLeave: userDoc.SickLeave,
                CasualLeave: userDoc.CasualLeave
            });
        });
    }
});

app.post('/leaveform', async (req, res) => {
    const {emailAddress, AnnualLeave, SickLeave, CasualLeave} = req.body;
    try {
        const userDoc = User.findOneAndUpdate({emailAddress}, {AnnualLeave, SickLeave, CasualLeave});
        res.json(userDoc);
    } catch (error) {
        console.error('Error updating users data:', error);
        res.status(500).json({error: 'Failed to update users data'});
    }
});
app.get('/profile', (req, res) => {
    const {token} = req.cookies;
    jwt.verify(token, secret,(err, decoded) => {
        if (err) {
            res.status(400).json({errorMessage: 'Please try again later'});
        } else {
            res.json(decoded);
        }
    })
});

app.post('/logout', (req, res) => {
    res.cookie('token', '').json('ok');
});

app.get('/user/:emailAddress', async (req, res) => {
    const {emailAddress} = req.params;
    try {
        const userDoc = await User.findOne({emailAddress});
        res.json(userDoc);
    } catch (error) {
        console.error('Error retrieving users data:', error);
        res.status(500).json({error: 'Failed to retrieve users data'});
    }
});

app.listen(4000);