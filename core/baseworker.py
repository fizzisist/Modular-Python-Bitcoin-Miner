# Modular Python Bitcoin Miner
# Copyright (C) 2012 Michael Sparmann (TheSeven)
#
#     This program is free software; you can redistribute it and/or
#     modify it under the terms of the GNU General Public License
#     as published by the Free Software Foundation; either version 2
#     of the License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Please consider donating to 1PLAPWDejJPJnY2ppYCgtw5ko8G5Q4hPzh if you
# want to support further development of the Modular Python Bitcoin Miner.



#####################
# Worker base class #
#####################



from threading import RLock
from .util import Bunch
from .inflatable import Inflatable



class BaseWorker(Inflatable):

  can_autodetect = False
  settings = dict(Inflatable.settings, **{
    "name": {"title": "Name", "type": "string", "position": 100},
  })


  def __init__(self, core, state = None, parent = None):
    super(BaseWorker, self).__init__(core, state)
    self.start_stop_lock = RLock()
    self.children = []
    self.parent = parent
    if parent: parent.children.add(self)
    self.jobs_per_second = 0
    self.parallel_jobs = 0
    
    
  def destroy(self):
    if self.parent: self.parent.children.remove(self)


  def apply_settings(self):
    super(BaseWorker, self).apply_settings()
    if not "name" in self.settings or not self.settings.name:
      self.settings.name = getattr(self.__class__, "default_name", "Untitled worker")

      
  def get_jobs_per_second(self):
    result = self.jobs_per_second
    for child in self.children: result += child.get_jobs_per_second()
    return result
      
  def get_parallel_jobs(self):
    result = self.parallel_jobs
    for child in self.children: result += child.get_parallel_jobs()
    return result