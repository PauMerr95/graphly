from config.parser import (
    build_default_config,
    generate_path,
    import_config_toml,
    parse_args,
)
from loaders import load_datafile
from plotting import MatplotlibPlotter


def main() -> None:
    args = parse_args()
    config = (
        import_config_toml(generate_path(args.config))
        if args.config is not None
        else build_default_config()
    )
    data = load_datafile(generate_path(args.filename))
    plotter = MatplotlibPlotter()
    figure = plotter.render(data, config)
    plotter.show(figure)


if __name__ == "__main__":
    main()
