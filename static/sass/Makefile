
SASSC=sassc -t compressed

all: ../css/style.css

../css/style.css: style.scss _main.scss _variables.scss _reset.scss
	$(SASSC) $< $@
