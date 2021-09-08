
class WIFI:
  
  def __init__(self, name='MYWIFI', pwd='66668888'):
    import network
    self.wifiname = name
    self.password = pwd
    self.wlan = network.WLAN(network.STA_IF)
    
  def do_connect(self):
    import network
    
    self.wlan.active(True)
    if not self.wlan.isconnected():
      print('connecting to network...')
      self.wlan.connect(self.wifiname, self.password)
      while not self.wlan.isconnected():
        pass
        
  def show_info(self):
    import network
    if(self.wlan != None):
      print('network config:', self.wlan.ifconfig())
    
  def isWifiConnected(self):
    import network
    return self.wlan.isconnected()
      
  def show_wlan(self):
    import network
    return self.wlan
    
    
