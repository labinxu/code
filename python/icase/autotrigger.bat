@rem Author: ext-laibin.xu@nokia.com
@rem trigger ut test for app gallery2
call python autotrigger.py --product "ara" --icase_mode "icase" --tests_proj_filter "Gallery2" --icase_svn_rel "svnrel" --target_build_variant "eng" --testtype "ut_self" 

@rem trigger self rfa
call python autotrigger.py --product "ara" --icase_svn_rel "" --target_build_variant "eng" --testtype "rfa_self" --icase_index "testcloud_self_run_index" --icase_mode "test_automation/system_tests/RFA" --icase_path "tools/test_automation"

call python autotrigger.py --product "ara" --icase_svn_rel "" --target_build_variant "eng" --testtype "rfa_self_split" --icase_index "marble_rfa_all_index" --icase_mode "test_automation/system_tests/RFA" --icase_path "tools/test_automation" --icase_split "4"



