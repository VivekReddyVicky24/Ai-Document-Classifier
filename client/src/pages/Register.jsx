import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/auth.css';

const getPasswordStrength = (pw) => {
  if (!pw) return null;
  let score = 0;
  if (pw.length >= 8) score++;
  if (/[A-Z]/.test(pw)) score++;
  if (/[0-9]/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw)) score++;
  if (score <= 1) return 'weak';
  if (score <= 3) return 'medium';
  return 'strong';
};

const Register = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validation
      if (!firstName || !lastName || !email || !password || !confirmPassword) {
        setError('Please fill in all fields');
        return;
      }

      if (firstName.trim().length < 2) {
        setError('First name must be at least 2 characters');
        return;
      }

      if (lastName.trim().length < 2) {
        setError('Last name must be at least 2 characters');
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        setError('Please enter a valid email address');
        return;
      }

      if (password.length < 6) {
        setError('Password must be at least 6 characters');
        return;
      }

      if (password !== confirmPassword) {
        setError('Passwords do not match');
        return;
      }

      await register(firstName, lastName, email, password);
      navigate('/dashboard');
    } catch (err) {
      const errorMessage = err.response?.data?.message || 'Registration failed. Please try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const pwStrength = getPasswordStrength(password);

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Create your account</h1>
          <p>Start classifying documents with AI</p>
        </div>

        {error && <div className="error-banner" role="alert">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form" noValidate>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">First name</label>
              <input
                type="text"
                id="firstName"
                autoComplete="given-name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="John"
                disabled={loading}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="lastName">Last name</label>
              <input
                type="text"
                id="lastName"
                autoComplete="family-name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Doe"
                disabled={loading}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="email">Email address</label>
            <input
              type="email"
              id="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-wrapper">
              <input
                type={showPw ? 'text' : 'password'}
                id="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Create a strong password"
                disabled={loading}
                required
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPw(!showPw)}
                aria-label={showPw ? 'Hide password' : 'Show password'}
              >
                {showPw ? '🙈' : '👁'}
              </button>
            </div>
            {pwStrength && (
              <div className="password-strength" aria-live="polite">
                <div className="strength-bar">
                  <div className={`strength-fill ${pwStrength}`}></div>
                </div>
                <span className={`strength-label ${pwStrength}`}>
                  {pwStrength === 'weak' && '⚡ Weak password'}
                  {pwStrength === 'medium' && '✓ Medium strength'}
                  {pwStrength === 'strong' && '✅ Strong password'}
                </span>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm password</label>
            <div className="password-wrapper">
              <input
                type={showConfirm ? 'text' : 'password'}
                id="confirmPassword"
                autoComplete="new-password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Repeat your password"
                disabled={loading}
                required
                style={confirmPassword && confirmPassword !== password
                  ? { borderColor: 'var(--danger)' } : {}}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowConfirm(!showConfirm)}
                aria-label="Toggle confirm password"
              >
                {showConfirm ? '🙈' : '👁'}
              </button>
            </div>
            {confirmPassword && confirmPassword !== password && (
              <span style={{ fontSize:'0.75rem', color:'var(--danger)', fontWeight:'500' }}>
                ✕ Passwords do not match
              </span>
            )}
            {confirmPassword && confirmPassword === password && (
              <span style={{ fontSize:'0.75rem', color:'var(--success)', fontWeight:'500' }}>
                ✓ Passwords match
              </span>
            )}
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? <><span className="spinner-sm"></span> Creating account…</> : 'Create account →'}
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account? <Link to="/login" className="auth-link">Sign in here</Link></p>
        </div>
      </div>
    </div>
  );
};

export default Register;
