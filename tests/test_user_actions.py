import unittest

from app import app, BC

class UserActionsTestCase(unittest.TestCase):
  def setUp(self):
    self.app = app.test_client()
    self.app.testing = True

  def login_as_user(self, username="userA", password="userApass"):
    return self.app.post(
      '/login',
      data=dict(username=username, password=password),
      follow_redirects=True
    )
  
  def test_create_batch(self):
    self.login_as_user()
    res = self.app.post(
      '/user/create',
      data={'batch_id': 'TEST-BATCH-1', 'info': 'Initial batch'},
      follow_redirects=True
    )
    self.assertEqual(res.status_code, 200)
    self.assertIn(b'Batch created successfully', res.data)

  def test_transfer_batch(self):
    self.login_as_user()
    self.app.post(
      '/user/create',
      data={'batch_id': 'TEST-BATCH-2', 'info': 'For transfer test'}
    )
    res = self.app.post(
      '/user/transfer',
      data={'batch_id': 'TEST-BATCH-2', 'to_user': 'UserB'},
      follow_redirects=True
    )
    self.assertEqual(res.status_code, 200)

  def test_view_history(self):
    self.login_as_user()
    res = self.app.get(
      '/user/history/TEST-BATCH-1',
      follow_redirects=True
    )
    self.assertEqual(res.status_code, 200)
    self.assertIn(b'History for Batch ID', res.data)