const { signup, login } = require('../controllers/AuthController.js');
const { signupValidation, loginValidation } = require('../middlewares/AuthMiddleware.js');
// const { getQuizData } = require('../Controllers/GeminiController.js');

const router = require('express').Router();

// User authentication routes
router.post('/login', loginValidation, login);
router.post('/signup', signupValidation, signup);

// Quiz data route (POST request because we're sending data in the body)
// router.post('/', getQuizData);
router.post('')
module.exports = router;