import argparse

from verif_spatial import DataModule


def get_parser():
    parser = argparse.ArgumentParser(description="Spatial verification of meteorological fields")
    parser.add_argument('path', type=str, nargs='+', help='Path or paths to fields, NetCDF or Zarr')
    parser.add_argument('-v', '--version', action='store_true', default=False)
    parser.add_argument('--list_times', action='store_true', default=False)
    parser.add_argument('--reference_time', action='store_true', default=False)

    parser.add_argument('-f', '--field', nargs='+', type=str, default=None, help='Field or fields to include')
    parser.add_argument('-o', '--lead_time', nargs='+', type=int, default=None, help='Lead times, given in multiples of frequency')
    parser.add_argument('-e', '--member', nargs='+', type=int, default=None, help='Member IDs to include')
    parser.add_argument('-l', '--label', nargs='+', type=str, default=None, help='Label(s) associated with path(s)')
    parser.add_argument('-r', '--res', type=float, default=None, help='Interpolation resolution')
    parser.add_argument('--ref', type=str, default=None, help='Reference time')
    parser.add_argument('--freq', type=str, default='6h', help='Temporal frequency between lead times')
    parser.add_argument('--path_out', type=str, default=None, help='Output path')
    parser.add_argument('-m', '--method', type=str, default=None, help='Analysis method to run')

    return parser

def run():
    args, unknown = get_parser().parse_known_args()

    unknown_dct = {}
    for element in unknown:
        print(element)
        #dct = string_to_nested_dict(element)
        #unknown_dct = merge(unknown_dct, dct)

    if args.version:
        print("Version")
        exit(0)

    dm = DataModule(
        path=args.path,
        field=args.field,
        lead_time=args.lead_time,
        member=args.member,
        label=args.label,
        interp_res=args.res,
        reference_time=args.ref,
        freq=args.freq,
    )


    if args.list_times:
        print("List times")
        exit(0)
    elif args.reference_time:
        print("Reference time")
        exit(0)

    match args.method:
        case 'plot':
            pt = Plot2d(dm.data_obj)
            pt.add_colormesh(
                    args.field, 
                    member=args.member,
                    lead_time=args.lead_time,
                    units='K',
                    cmap='turbo',
            )
            #pt.add_contour_lines('air_pressure_at_sea_level')
            pt(path_out=args.path_out)
        case _:
            exit(0)
