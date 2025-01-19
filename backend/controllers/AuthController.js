const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
require('dotenv').config();
const { v4: uuid } = require('uuid'); // For generating unique user IDs
const client = require('../config/db.js');

// Signup Function
const signup = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    // Check if user already exists
    const query = 'SELECT email FROM social_media_engagement.users WHERE email = ? ALLOW FILTERING';
    const user = await client.execute(query, [email], { prepare: true });

    if (user.rowLength > 0) {
      return res.status(409).json({ msg: "User already exists, you can login", success: false });
    }

    // Encrypt password
    const encryptedPass = await bcrypt.hash(password, 10);

    // Insert new user
    const insertQuery = `INSERT INTO social_media_engagement.users (user_id, email,password,username) VALUES (?, ?, ?, ?)`;
    await client.execute(insertQuery, [uuid(), email,encryptedPass,name], { prepare: true });

    return res.status(200).json({ msg: "Signup Success", success: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ msg: "Internal server error", success: false });
  }
};

// Login Function
const login = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Retrieve user from database
    const query = 'SELECT user_id, username, email, password FROM social_media_engagement.users WHERE email = ? ALLOW FILTERING';
    const result = await client.execute(query, [email], { prepare: true });

    if (result.rowLength === 0) {
      return res.status(403).json({
        msg: "Authentication Failed: Email or Password is wrong",
        success: false,
      });
    }

    const user = result.rows[0];

    // Compare passwords
    const isPassEqual = await bcrypt.compare(password, user.password);
    if (!isPassEqual) {
      return res.status(403).json({
        msg: "Authentication Failed: Email or Password is wrong",
        success: false,
      });
    }

    // Generate JWT
    const jwToken = jwt.sign(
      { email: user.email, id: user.id },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.status(200).json({
      msg: "Login Success",
      success: true,
      jwToken,
      email: user.email,
      name: user.name,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ msg: "Internal server error", success: false });
  }
};

module.exports = {
  signup,
  login,
};
