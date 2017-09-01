build: public public/tachyons.css public/styles.css
	node dashboard.js

public:
	mkdir -vp public

public/tachyons.css: public node_modules/tachyons/css/tachyons.min.css
	cp node_modules/tachyons/css/tachyons.min.css public/tachyons.css

public/styles.css: dashboard/styles.css
	cp dashboard/styles.css public/styles.css

clean:
	rm -rf ./public

.PHONY: build clean
