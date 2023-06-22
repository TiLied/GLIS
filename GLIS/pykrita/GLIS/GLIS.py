from krita import *

class MyExtension(Extension):
	
	def __init__(self, parent):
		super().__init__(parent)

	def setup(self):
		pass

	def createActions(self, window):
		action = window.createAction("GLIS_ID", "GLIS", "tools/scripts")
		action.triggered.connect(self.GLIS)
		
	def GLIS(self):
		
		doc = Krita.instance().activeDocument()
		root = doc.rootNode()
		currentLayer = doc.activeNode()
		parent = currentLayer
		arr = []
				
		if doc is not None:
			_dup_ = doc.nodeByName("_dup_") 
			if "None" not in str(_dup_):
				_dup_.remove()
				doc.refreshProjection()
				return
		
			while True:
				if "None" in str(parent):
					break
				parent = parent.parentNode()
				arr.append(parent)
			
			l = len(arr) - 3
			if l <= -1:
				return
			
			dup = arr[l].duplicate()
			dup.setName("_dup_")
			dup.setBlendingMode("inc_saturation")
			dup.setLocked(True)
			
			root.addChildNode(dup, arr[l])
			
			childs = root.childNodes()
			_fake_ = doc.createGroupLayer("_fake_")
			root.addChildNode(_fake_, childs[0])
		
			childs = root.childNodes()
			dupFirstL = childs[0].duplicate()
			root.removeChildNode(childs[0])
			
			childs = root.childNodes()
			root.addChildNode(dupFirstL, childs[0])
			
			childs = root.childNodes()
			root.setChildNodes(childs)
			
			doc.setActiveNode(currentLayer)
			
			_fake_ = doc.nodeByName("_fake_") 
			if "None" not in str(_fake_):
				_fake_.remove()
				
			doc.refreshProjection()

Krita.instance().addExtension(MyExtension(Krita.instance()))