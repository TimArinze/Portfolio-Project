const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    firstName: {type: String, required: true, trim: true, minlength: 3},
    lastName: {type: String, required: true, trim: true, minlength: 3},
    emailAddress: {type: String, required: true, trim: true, unique: true},
    employeeID: {type: String, required: true, trim: true, unique: true},
    DOB: {type: Date, required: true},
    department: {type: String, required: true,},
    password: {type: String, required: true, trim: true, minlength: 3},
}, {timestamps: true});


const User = mongoose.model('User', UserSchema);

module.exports = User;