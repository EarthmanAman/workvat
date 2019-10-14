from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse



class StaticViewSitemap(Sitemap):
	def items(self):
		return ['index', 'services', 'about', 'contact']

	def location(self, obj):
		try:
			return reverse("assignment:%s" % obj)
		except:
			return reverse("accounts:%s" % obj )