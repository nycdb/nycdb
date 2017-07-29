build: public public/tachyons.css
	node build.js

public:
	mkdir -vp public

public/tachyons.css: public node_modules/tachyons/css/tachyons.min.css
	cp node_modules/tachyons/css/tachyons.min.css public/tachyons.css

clean:
	rm -rf ./public

.PHONY: build clean
