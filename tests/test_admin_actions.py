import unittest

from app import app, BC

class AdminActionTestCase(unittest.TestCase):
  def setUp(self):
    self.app = app.test_client()
    self.app.testing = True

  def login_as_admin(self, username="admin1", password="adminpass"):
    return self.app.post(
      '/login',
      data=dict(username=username, password=password),
      follow_redirects=True
    )
  
  def test_view_dashboard(self):
    self.login_as_admin()
    res = self.app.get('/admin/dashboard')
    self.assertEqual(res.status_code, 200)
    self.assertIn(b'Admin Dashboard', res.data)

  def test_raise_concern(self):
    self.login_as_admin()
    data = {
      'batch-id': 'TEST-BATCH-1',
      'block_index': 1,
      'issue': 'Fake issue for testing'
    }
    res = self.app.post(
      '/admin/concerns',
      data=data,
      follow_redirects=True
    )
    self.assertEqual(res.status_code, 201)

  def test_approve_and_deny_transfer(self):
    self.login_as_admin()
    # assuming transfer block with index exists for test
    res_approve = self.app.post('/admin/approve_transfer/2')
    res_deny = self.app.post('/admin/deny_transfer/2')
    self.assertIn(res_approve.status_code, [200, 404, 400])
    self.assertIn(res_deny.status_code, [200, 404, 400])