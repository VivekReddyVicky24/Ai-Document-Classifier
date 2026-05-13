const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

const validateEmail = (email) => {
  return emailRegex.test(email);
};

const validatePassword = (password) => {
  if (!password || password.length < 6) {
    return false;
  }
  return true;
};

const validateName = (name) => {
  if (!name || name.trim().length < 2 || name.trim().length > 50) {
    return false;
  }
  return true;
};

module.exports = {
  validateEmail,
  validatePassword,
  validateName,
};
