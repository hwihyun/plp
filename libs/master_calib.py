import os
import numpy as np
import json


def get_master_calib_abspath(fn):
    return os.path.join("master_calib", fn)


def load_thar_ref_data(ref_date, band):
    # load spec

    igrins_orders = {}
    igrins_orders["H"] = range(99, 122)
    igrins_orders["K"] = range(72, 92)

    ref_spec_file = "arc_spec_thar_%s_%s.json" % (band, ref_date)
    ref_id_file = "thar_identified_%s_%s.json" % (band, ref_date)

    s_list_ = json.load(open(get_master_calib_abspath(ref_spec_file)))
    s_list_src = [np.array(s) for s in s_list_]

    # reference line list : from previous run
    ref_lines_list = json.load(open(get_master_calib_abspath(ref_id_file)))

    r = dict(ref_date=ref_date,
             band=band,
             ref_spec_file=ref_spec_file,
             ref_id_file=ref_id_file,
             ref_lines_list=ref_lines_list,
             ref_s_list=s_list_src,
             orders=igrins_orders[band])

    return r



def load_sky_ref_data(ref_utdate, band):
    json_name = "ref_ohlines_indices_%s.json" % (ref_utdate,)
    fn = get_master_calib_abspath(json_name)
    ref_ohline_indices_map = json.load(open(fn))
    ref_ohline_indices = ref_ohline_indices_map[band]

    ref_ohline_indices = dict((int(k), v) for k, v \
                              in ref_ohline_indices.items())

    from oh_lines import OHLines
    fn = get_master_calib_abspath("ohlines.dat")
    ohlines = OHLines(fn)

    # from fit_gaussian import fit_gaussian_simple


    r = dict(ref_date=ref_utdate,
             band=band,
             ohlines_db = ohlines,
             ohline_indices=ref_ohline_indices,
             )

    return r
