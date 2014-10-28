
def GetCoreShortcodes(r_dep_shortcode_,core_shortcode_vec_ ):
    if r_dep_shortcode_=='ZN_0' or r_dep_shortcode_=='ZB_0':
        if not "FGBL_0" in core_shortcode_vec_ :
            core_shortcode_vec_.append("FGBL_0")
        if not "ZB_0" in core_shortcode_vec_ :
            core_shortcode_vec_.append("ZB_0")
        if not "ZF_0" in core_shortcode_vec_ :
            core_shortcode_vec_.append("ZF_0")
        if not "ES_0" in core_shortcode_vec_ :
            core_shortcode_vec_.append("ES_0")
        if not r_dep_shortcode_ in core_shortcode_vec_ :
            core_shortcode_vec_.append(r_dep_shortcode_)
            