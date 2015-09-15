all: install

install:
	@cp -v src/auto-wallpaper.py /usr/sbin/
	@mv /usr/sbin/auto-wallpaper.py /usr/sbin/auto-wallpaper
	@cp -v init.d/auto-wallpaper /etc/init.d/
	@update-rc.d auto-wallpaper defaults 95
	

uninstall:
	@rm -v /usr/sbin/auto-wallpaper
	@rm -v /etc/init.d/auto-wallpaper
	@update-rc.d auto-wallpaper remove
