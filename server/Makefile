MARKDOWN = pandoc --from gfm --to html --standalone -H style.css.html

index.html: index.md style.css.html
	$(MARKDOWN) $< --output $@

style.css.html: style.css
	echo "<style>" > style.css.html
	cat style.css >> style.css.html
	echo "</style>" >> style.css.html
