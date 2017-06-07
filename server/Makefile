MARKDOWN = pandoc --from markdown_github --to html --standalone -H style.css.html

index.html: index.md style.css.html
	$(MARKDOWN) $< --output $@

setup: postgrest

postgrest: postgrest-0.4.1.0-ubuntu.tar.xz
	tar xf postgrest-0.4.1.0-ubuntu.tar.xz	

postgrest-0.4.1.0-ubuntu.tar.xz:
	wget https://github.com/begriffs/postgrest/releases/download/v0.4.1.0/postgrest-0.4.1.0-ubuntu.tar.xz

style.css.html: style.css
	echo "<style>" > style.css.html
	cat style.css >> style.css.html
	echo "</style>" >> style.css.html
