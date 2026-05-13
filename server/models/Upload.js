const mongoose = require('mongoose');

const uploadSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'User ID is required'],
    },
    originalFileName: {
      type: String,
      required: [true, 'File name is required'],
      trim: true,
    },
    predictedLabel: {
      type: String,
      required: [true, 'Predicted label is required'],
    },
    confidence: {
      type: Number,
      min: 0,
      max: 100,
    },
    filePath: {
      type: String,
      default: null,
    },
    fileSize: {
      type: Number,
      default: null,
    },
    status: {
      type: String,
      enum: ['uploaded', 'processing', 'completed', 'failed'],
      default: 'uploaded',
    },
    error: {
      type: String,
      default: null,
    },
  },
  {
    timestamps: true,
  }
);

// Index for efficient queries
uploadSchema.index({ userId: 1, createdAt: -1 });

// Populate user data when querying
uploadSchema.pre(/^find/, function () {
  this.populate('userId', 'name email');
});

module.exports = mongoose.model('Upload', uploadSchema);
