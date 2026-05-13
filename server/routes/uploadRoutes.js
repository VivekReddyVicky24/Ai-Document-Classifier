const express = require('express');
const multer = require('multer');
const path = require('path');
const {
  uploadFile,
  getUploadHistory,
  getUpload,
  deleteUpload,
  downloadUpload,
  viewUpload,
} = require('../controllers/uploadController');
const protect = require('../middleware/authMiddleware');

const router = express.Router();

// Multer configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = process.env.UPLOAD_TEMP_DIR || './uploads/temp';
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const timestamp = Date.now();
    const originalName = file.originalname.replace(/\s+/g, '_');
    cb(null, `${timestamp}-${originalName}`);
  },
});

const fileFilter = (req, file, cb) => {
  // Only allow PDF files
  if (file.mimetype === 'application/pdf' || file.originalname.endsWith('.pdf')) {
    cb(null, true);
  } else {
    cb(new Error('Only PDF files are allowed'), false);
  }
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: parseInt(process.env.MAX_FILE_SIZE || 10485760), // 10MB default
  },
});

// Protected routes
router.post(
  '/',
  protect,
  (req, res, next) => {
    upload.array('files', 10)(req, res, (err) => {
      if (err) {
        if (err.code === 'LIMIT_FILE_SIZE') {
          return res.status(400).json({
            success: false,
            message: 'File size exceeds maximum limit (10MB)',
          });
        }
        if (err.code === 'LIMIT_FILE_COUNT') {
          return res.status(400).json({
            success: false,
            message: 'Maximum 10 files allowed',
          });
        }
        return res.status(400).json({
          success: false,
          message: err.message || 'File upload error',
        });
      }
      next();
    });
  },
  uploadFile
);
router.get('/history', protect, getUploadHistory);
router.get('/:id/download', protect, downloadUpload);
router.get('/:id/view', protect, viewUpload);
router.get('/:id', protect, getUpload);
router.delete('/:id', protect, deleteUpload);

module.exports = router;
