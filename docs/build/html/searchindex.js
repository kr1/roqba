Search.setIndex({envversion:46,filenames:["behaviour_dict","composers","director","drummer","events_and_messages","gui_connect","index","main","melodic_behaviours","melody_player","meters","metronome","movement_probabilities","notator","note_gateway","note_length_groupings","overview","pd_wavetables","pdsender","roqba","scales_and_harmonies","settings","sine_controllers","static","utilities","voice"],objects:{"roqba.composers":{abstract_composer:[1,0,0,"-"],amadinda:[1,0,0,"-"],baroq:[1,0,0,"-"],rendezvous:[1,0,0,"-"]},"roqba.composers.abstract_composer":{AbstractComposer:[1,2,1,""]},"roqba.composers.abstract_composer.AbstractComposer":{assemble_real_scale:[1,5,1,""],choose_rhythm:[1,1,1,""],generate:[1,1,1,""],generate_real_scale:[1,1,1,""],report:[1,1,1,""],set_binaural_diffs:[1,1,1,""],set_meter:[1,1,1,""],set_scale:[1,1,1,""]},"roqba.composers.amadinda":{Composer:[1,2,1,""]},"roqba.composers.amadinda.Composer":{all_python_words:[1,1,1,""],choose_rhythm:[1,1,1,""],generate:[1,1,1,""],make_new_pattern:[1,1,1,""],next_voice_note:[1,1,1,""],shift_pattern:[1,1,1,""]},"roqba.composers.baroq":{Composer:[1,2,1,""]},"roqba.composers.baroq.Composer":{acceptable_harm_for_length:[1,1,1,""],acceptable_harmony:[1,1,1,""],add_duration_in_msec:[1,1,1,""],apply_scale:[1,1,1,""],embellish:[1,1,1,""],flatten_chord:[1,5,1,""],generate:[1,1,1,""],get_deltas:[1,5,1,""],is_base_harmony:[1,1,1,""],ornament_handler:[1,1,1,""],scale_walker:[1,5,1,""],sort_voices_by_importance:[1,1,1,""],stream_analyzer:[1,1,1,""]},"roqba.composers.rendezvous":{Composer:[1,2,1,""],random:[1,3,1,""]},"roqba.composers.rendezvous.Composer":{determine_rendezvous_transition:[1,1,1,""],generate:[1,1,1,""],next_voice_note:[1,1,1,""],select_next_anchor_tick:[1,1,1,""],select_next_harmony:[1,1,1,""]},"roqba.director":{Director:[2,2,1,""],random:[2,3,1,""]},"roqba.director.Director":{add_setters:[2,1,1,""],check_incoming_messages:[2,1,1,""],make_length:[2,1,1,""],new_microspeed_sine:[2,1,1,""],new_random_meter:[2,1,1,""],pause:[2,1,1,""],set_meter:[2,1,1,""],stop:[2,1,1,""],unpause:[2,1,1,""]},"roqba.drummer":{ContFrame:[3,2,1,""],Drummer:[3,2,1,""],random:[3,3,1,""]},"roqba.drummer.ContFrame":{confirm:[3,4,1,""],ctl2:[3,4,1,""],ctl:[3,4,1,""],meta:[3,4,1,""],pan2:[3,4,1,""],pan:[3,4,1,""],vol:[3,4,1,""]},"roqba.drummer.Drummer":{cont_frame:[3,1,1,""],create_pattern:[3,1,1,""],empty_pattern:[3,1,1,""],generate:[3,1,1,""],high_low_seq:[3,1,1,""],mark_frame:[3,1,1,""],push_value:[3,1,1,""],smoothen:[3,1,1,""]},"roqba.main":{main:[7,3,1,""]},"roqba.metronome":{Metronome:[11,2,1,""]},"roqba.metronome.Metronome":{beat:[11,1,1,""],reset:[11,1,1,""],set_meter:[11,1,1,""]},"roqba.notator":{Notator:[13,2,1,""]},"roqba.notator.Notator":{add_note:[13,1,1,""],draw:[13,1,1,""],get_unix_scroll_command:[13,1,1,""],make_matrix:[13,1,1,""],notate_bar_sequence:[13,1,1,""],notate_rhythm:[13,1,1,""],note_to_file:[13,1,1,""],post_process:[13,1,1,""],reset:[13,1,1,""],write_to_file:[13,1,1,""]},"roqba.note_gateway":{NoteGateway:[14,2,1,""]},"roqba.note_gateway.NoteGateway":{drum_hub_gen:[14,1,1,""],hub_gen:[14,1,1,""],mute_voice:[14,1,1,""],pause:[14,1,1,""],pd_send_drum_note:[14,1,1,""],pd_send_duration:[14,1,1,""],pd_send_note:[14,1,1,""],pd_send_wavetable:[14,1,1,""],send_voice_adsr:[14,1,1,""],send_voice_pan:[14,1,1,""],send_voice_peak_level:[14,1,1,""],send_voice_volume:[14,1,1,""],set_slide_msecs:[14,1,1,""],set_slide_msecs_for_all_voices:[14,1,1,""],set_slide_to_0:[14,1,1,""],set_transpose:[14,1,1,""],stop:[14,1,1,""],stop_all_notes:[14,1,1,""],stop_notes_of_voice:[14,1,1,""],unpause:[14,1,1,""]},"roqba.static":{"__init__":[23,0,0,"-"],melodic_behaviours:[8,0,0,"-"],meters:[10,0,0,"-"],movement_probabilities:[12,0,0,"-"],note_length_groupings:[15,0,0,"-"],scales_and_harmonies:[20,0,0,"-"],settings:[21,0,0,"-"]},"roqba.static.note_length_groupings":{analyze_grouping:[15,3,1,""],badly_formeD:[15,3,1,""],cut_grouping_to_size:[15,3,1,""],get_grouping:[15,3,1,""]},"roqba.static.settings":{flatten_meters:[21,3,1,""]},"roqba.utilities":{"__init__":[24,0,0,"-"],behaviour_dict:[0,0,0,"-"],gui_connect:[5,0,0,"-"],melody_player:[9,0,0,"-"],pd_wavetables:[17,0,0,"-"],pdsender:[18,0,0,"-"],sine_controllers:[22,0,0,"-"]},"roqba.utilities.behaviour_dict":{BehaviourDict:[0,2,1,""],test_setter:[0,3,1,""]},"roqba.utilities.behaviour_dict.BehaviourDict":{read_or_create_saved_behaviours:[0,1,1,""],save_current_behaviour:[0,1,1,""],voice_get:[0,1,1,""],write_saved_behaviours:[0,1,1,""]},"roqba.utilities.gui_connect":{GuiConnect:[5,2,1,""]},"roqba.utilities.gui_connect.GuiConnect":{handle_caesura:[5,1,1,""],read_incoming_messages:[5,1,1,""],send:[5,1,1,""],send_cycle_pos:[5,1,1,""],update_gui:[5,1,1,""]},"roqba.utilities.melody_player":{MelodyPlayer:[9,2,1,""],extract_modified_move:[9,3,1,""]},"roqba.utilities.melody_player.MelodyPlayer":{play:[9,1,1,""]},"roqba.utilities.pd_wavetables":{harmonic_wavetable:[17,3,1,""],random_harmonic_wavetable:[17,3,1,""],random_wavetable:[17,3,1,""]},"roqba.utilities.pdsender":{PdSender:[18,2,1,""],Sender:[18,2,1,""]},"roqba.utilities.pdsender.PdSender":{format_msg_list:[18,5,1,""],send:[18,1,1,""]},"roqba.utilities.pdsender.Sender":{trace_send:[18,1,1,""]},"roqba.utilities.sine_controllers":{MultiSine:[22,2,1,""],Sine:[22,2,1,""]},"roqba.utilities.sine_controllers.MultiSine":{assemble_funnel:[22,1,1,""],get_value:[22,1,1,""],get_value_as_factor:[22,1,1,""],set_freqs:[22,1,1,""]},"roqba.utilities.sine_controllers.Sine":{get_value:[22,1,1,""],set_freq:[22,1,1,""]},"roqba.voice":{Voice:[25,2,1,""]},"roqba.voice.Voice":{add_setters_for_behaviour_dict:[25,1,1,""],apply_overhanging_notes:[25,1,1,""],exceeds:[25,1,1,""],in_the_middle:[25,1,1,""],make_wavetable:[25,1,1,""],manage_melody_note:[25,1,1,""],new_microvolume_sine:[25,1,1,""],next_note:[25,1,1,""],register_other_voices:[25,1,1,""],reload_register:[25,1,1,""],reset_slave:[25,1,1,""],search_suitable_melody:[25,1,1,""],set_note_length_groupings:[25,1,1,""],set_pan_pos:[25,1,1,""],set_rhythm_grouping:[25,1,1,""],update_current_microvolume:[25,1,1,""],voice:[25,1,1,""]},roqba:{"__init__":[19,0,0,"-"],director:[2,0,0,"-"],drummer:[3,0,0,"-"],main:[7,0,0,"-"],metronome:[11,0,0,"-"],notator:[13,0,0,"-"],note_gateway:[14,0,0,"-"],voice:[25,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","method","Python method"],"2":["py","class","Python class"],"3":["py","function","Python function"],"4":["py","attribute","Python attribute"],"5":["py","staticmethod","Python static method"]},objtypes:{"0":"py:module","1":"py:method","2":"py:class","3":"py:function","4":"py:attribute","5":"py:staticmethod"},terms:{"1x1":15,"1x2":15,"1x3":15,"1x4":15,"1x5":15,"1x6":15,"1x7":15,"1x8":15,"2x1":15,"2x2":15,"2x3":15,"3x1":15,"3x2":15,"4x1":15,"4x2":15,"5x1":15,"6th":12,"6x1":15,"8th":12,"8x1":15,"__assembl":17,"__main__":[8,20],"__name__":[8,20],"__setitem__":0,"_apply_wavet":17,"_as_float":17,"_assembl":15,"_composers_":16,"_plai":[4,16],"abstract":[],"boolean":21,"break":15,"case":15,"class":[],"default":[0,8,15],"final":16,"float":17,"function":[1,3,14,15,17,22],"import":[1,8,12,16,17,20,21],"int":[5,15,21,25],"long":21,"new":[1,4,14,15,22,25],"return":[0,1,4,11,15,17,22,25],"static":[],"true":[0,8,15,21,22,25],abstract_compos:1,abstractcompos:1,acceptable_harm_for_length:1,acceptable_harmoni:1,accord:[1,14,25],action:1,activ:14,add:[0,1],add_duration_in_msec:1,add_not:13,add_sett:2,add_setters_for_behaviour_dict:25,add_voic:[],adjust:16,adsr:[14,21],after:[],again:14,alia:3,all:[3,14,15,17,21],all_python_word:1,all_strict_harmoni:20,allow:3,also:[1,16,25],alt:21,alto:8,amadinda:[],amplitud:17,analys:1,analyz:16,analyze_group:15,ani:[1,22],anoth:4,app:[16,25],append:[3,15,17],appli:[10,17,25],applic:7,apply_overhanging_not:[4,25],apply_scal:[1,4],area:25,arg:0,around:22,arrai:[1,17],assembl:[3,15,17,22,25],assemble_funnel:22,assemble_real_scal:1,assert:[],attribut:[1,4,8,9,25],audio:[],audiobuf:[],aulo:21,autom:4,automate_adsr:21,automate_binaural_diff:21,automate_met:21,automate_microspeed_chang:21,automate_microvolume_chang:21,automate_note_duration_min_max:21,automate_note_duration_prop:21,automate_num_parti:21,automate_pan:21,automate_scal:21,automate_slid:21,automate_speed_chang:21,automate_transpos:21,automate_wavet:21,autonom:21,averag:21,back:25,background:[],badli:15,badly_form:15,bar_sequ:21,baroq:[],base:[],base_harmoni:20,basic:4,bass:[3,8,21,25],bass_chord_distance_prob:12,bass_movement_prob:[8,12],bass_prob:12,beat:[4,5,11,15],been:0,befor:0,behaviour:[0,1,2,14,16,21,25],behaviourdict:[0,21],belong:25,between:[1,21],binari:15,binaur:[4,21],binaural_diff:21,bit:25,block:14,bool:15,both:16,bounc:25,bound:1,buffer_length:13,bulgarian:21,bypass:14,caesura:[4,5,16],caesura_prob:21,calcul:[22,25],call:[],can:[1,9,16,21],capabl:17,cat:16,ceasura:16,center:25,chang:[1,3],change_mast:25,change_rhythm_after_tim:8,check:[0,1,2,15,16,21],check_incoming_messag:[2,4],choic:4,choos:[],choose_rhythm:[1,4],chord:1,chosen:[1,25],clock:16,code:1,coeffici:25,combin:[15,22],come:[],command:[],comment:4,common:[],common_adsr:21,common_binaural_diff:21,common_note_dur:21,common_transit:21,common_wavet:21,commun:14,complet:5,compli:4,concern:14,condit:16,configur:1,confirm:3,consecut:17,conserv:21,consid:[],consist:3,constant:[10,15],constraint:21,cont:3,cont_fram:3,contain:[10,12,14,16,23,24],content:6,context:1,contfram:3,continu:[3,16],control:[14,16,22,24,25],coroutin:[4,16],correct:1,counter:11,crash:3,creat:[0,1,3,4,8,9,17,20,21,25],create_pattern:3,creation:3,creb:[],ctl2:3,ctl:[3,14],cumul:4,current:[0,1,11,25],custom:[0,24],cut:15,cut_grouping_to_s:15,cycle_po:[4,13],cymbal:3,data:[13,16,23],datagram:18,dataobject:[],decis:4,def:[15,17,21],default_behaviour:21,default_embellishment_prob:21,default_fast_group:15,default_group:[8,25],default_meter_length:15,default_movement_prob:[8,12],default_note_duration_prop:21,default_note_length_group:15,default_num_parti:21,default_pan_posit:21,default_pause_prob:21,default_prob:12,default_slower_group:15,default_ternary_group:15,default_volum:21,defin:[0,3,9],definit:17,deken:16,delta:[1,25],densiti:3,depend:[],destroi:14,det:17,determin:17,determine_rendezvous_transit:1,diagram:[],diaton:[1,8,20,21],dict:[0,3,5,24],dictionari:0,diff:[4,15,21],dir:1,direct:[1,21,25],disharm:20,doctest:[],downward:21,draw:13,drum:[3,4,14,16],drum_fil:12,drum_fill_handl:[],drum_hub:[],drum_hub_gen:14,drum_mark_handl:[],drummer:[],dual:21,duplic:3,durat:[1,4,14,21],dure:[15,23],dynam:20,each:[1,4,17],eadsr:[],either:1,elaps:22,els:15,embellish:[1,4,16],embellishment_prob:8,embellishment_speed_lim:21,empti:3,empty_pattern:3,enable_adsr:21,encod:5,engin:[4,9,14],enharmon:1,entri:15,enumer:17,environ:[8,21],equal:[15,22],equal_pow:22,etc:[3,24],even:[17,21],eventu:[4,25],everi:[0,5,15],exampl:16,exce:25,execut:23,exist:15,expect:17,experiment:20,extend:[1,12],extern:16,extract_modified_mov:9,fallback:[3,15],fals:[15,21,25],fast:[1,21],fast_group:[8,25],field:3,file:[0,9,16,21],filenam:13,fill:16,filter:15,first:[1,15,21],fix:21,fixed_meter_playalong:21,fixed_rendezvous_length:21,flag:[1,16],flat_mid:[8,21,25],flat_mid_movement_prob:[8,12],flat_mid_prob:12,flatspac:[],flatten_chord:1,flatten_met:21,flow:14,folder:16,follow:[4,16,20,25],follow_bar_sequ:21,form:15,format:[1,3,15,18],format_msg_list:18,found:15,four_note_harmoni:20,frame:[3,4,16],freq:22,frequenc:22,from:[3,8,12,14,16,21,25],from_gui_port:21,fun:17,further:[],gate:15,gatewai:[1,2,4,16,25],gener:[1,3,4,14,16,25],generate_real_scal:1,get:[],get_delta:1,get_group:15,get_unix_scroll_command:13,get_valu:22,get_value_as_factor:22,given:[0,1,3,9,14,15,16,17,21,22],gpan:[],graphic:16,greek:1,greek_chromat:[20,21],greek_enharmon:[20,21],group:[8,15,21,25],gui:[5,21],gui_host:21,guiconnect:5,half_beat:21,handl:1,handle_caesura:5,handle_incoming_messag:[],happen:5,harm:1,harmo_index:17,harmon:[1,4,16,17,20,21],harmoni:[1,4,20,23],harmonic_interv:20,harmonic_wavet:17,has_percuss:21,hat:3,have:[1,4,17],hear:9,heavi:[4,8,15],heavy_group:[8,25],helper:17,here:[1,25],hertz:1,high:[3,8,21,25],high_low_seq:3,highest_note_num:21,hold:8,host:18,how:21,html:[],hub:4,hub_gen:14,human:10,imp:1,implement:15,implic:15,in_rang:21,in_the_middl:25,incom:[2,5,17,18,25],index:[1,6,17],info:1,initi:3,instal:16,instanc:[1,9],interfac:[],intern:11,interv:[1,2,3],introduct:[],ipython:16,is_base_harmoni:1,item:15,itertool:[12,20],join:17,json:5,keep:21,kei:[0,3,5,15,21],kernel:[],keyerror:15,known:[],kwarg:0,lambda:[15,17],last:15,later:4,lax:21,lead:8,leap:21,legato_prob:8,length:[1,15,16,17,21,25],let:14,librari:16,like:23,limit:25,list:[12,17,18,20,21,22],load:15,local:21,local_set:21,localhost:21,log:16,loop:[3,16],low:3,low_mid:[8,21,25],lowest_note_num:21,made:4,main:[],mainli:0,major:1,make_length:2,make_matrix:13,make_new_pattern:1,make_wavet:25,manage_melody_not:25,manual:[],map:[1,17,25],mark:3,mark_fram:3,marker:[1,3],master:25,mat:13,math:17,max:[1,17,21,25],max_:17,max_adsr:21,max_binaural_diff:21,max_num_parti:21,max_rendezvous_length:21,max_rendezvous_tickoffset:21,max_shuffl:[10,21],max_spe:21,maximum:17,mean:21,melod:[8,14,20],melodi:[3,9,12,21,25],melodic_behaviour:[],melody_set:8,melodyplay:9,messag:[2,5,9,14,16,17,18],meta:3,meter:[],meter_filenam:13,meter_length:15,meter_monitor:13,meter_po:[1,25],method:[0,1,3,4,14,16,22,25],metronom:[],microspeed_max_speed_in_hz:21,microspeed_vari:21,microvolume_max_speed_in_hz:21,microvolume_vari:21,mid:[8,21,25],mid_prob:12,middl:21,middle_voices_movement_prob:[8,12],millisec:14,millisecond:1,min:[1,17,21,25],min_adsr:21,min_rendezvous_length:21,min_rendezvous_tickoffset:21,min_spe:21,minor:1,mode:15,modifi:[0,1,16,25],modprob:[],modul:[0,6,8,10,12,15,16,22,23,24],moment:22,motex:[],move:[4,9,25],movement:[8,21,23],movement_prob:[],msec:[14,21],msg:[5,14,18],multipl:22,multisin:22,must:22,mute:14,mute_voic:14,name:[0,1,8,21],necess:4,necessari:[9,15,16],need:16,neg:15,new_microspeed_sin:2,new_microvolume_sin:25,new_random_met:[2,4],new_spe:[],next:[1,4,25],next_not:25,next_voice_not:1,nin:15,nmode:15,noadc:[],non:15,none:[0,1,3,15,25],normal:[4,17],notat:[],notate_bar_sequ:13,notate_rhythm:13,note:[1,4,13,14,15,16,21,22,25],note_delta:1,note_duration_prop:4,note_gatewai:[],note_length_group:[],note_rang:25,note_to_fil:[4,13],notegatewai:14,notes_per_scal:20,npattern:15,num:17,num_lin:13,num_rendezvous_between_caesura:21,num_ton:[],num_voic:13,number:[3,17,21,22],number_of_tones_in_3rd_voic:21,number_of_voic:21,object:[14,16,22],obtain:16,octav:1,octave_offset:21,odd:[15,17,21],off:[14,25],offset:1,on_off_pattern:25,onli:23,open:16,origin:22,ornament:[1,12],ornament_handl:1,oscil:22,oss:[],other:[15,25],other_voic:[],otherwis:[0,25],out:[1,14],outgo:21,over:[1,5,21],overhang:25,overlaid:22,overridden:21,overview:[],padsp:[],page:6,pan2:3,pan:[3,4,14,21],pan_controls_binaural_diff:21,pan_po:25,parallel:21,param:25,part:17,partial:17,particular:[],patt:3,pattern:[3,15,25],paus:[2,14,15,16],pause_prob:8,pcm:[],pd_host:21,pd_port:21,pd_send_drum_not:14,pd_send_dur:14,pd_send_not:14,pd_send_wavet:14,pd_wavet:[],pdsender:[],peak_level:14,penta:8,penta_minor:[8,20],pentaton:20,per_voic:21,percussion_hub:4,perform:16,permut:[12,20],pi_step:17,pitch:25,place:4,plai:[9,16],plugin:16,polyphon:[1,4],pop:15,port:18,posit:[4,5,13],possibl:21,post:3,post_process:13,pprint:[],predominantli:21,prepend:[],present:[0,14],present_not:1,prevail:21,print:[1,8,20],privid:15,probabl:[12,23],process:[],produc:[1,22],product:[14,16],prop:4,proport:21,provid:22,pure:16,puredata:[14,16,17],purpos:14,push_valu:3,python:16,quarter:21,queue:2,rais:15,random:[1,2,3,17,21,25],random_harmon:21,random_harmonic_wavet:17,random_wavet:17,randomli:[1,17],rang:[1,8,21,22,25],raw:5,read:[0,5,23,25],read_incoming_messag:5,read_or_create_saved_behaviour:0,readm:[],real:1,real_not:25,real_scal:9,reappli:25,recommend:16,reconsid:15,regist:[0,1,4,8,25],register_other_voic:25,relat:[3,21,25],reli:16,reload:25,reload_regist:[1,25],rendezv:[],repeat:16,report:1,repres:17,represent:16,requir:15,reset:[4,11,13,25],reset_slav:25,result:16,resum:16,retriev:25,rhythm:15,rhythmic:[],ride:3,rock:21,rock_bass:[8,21,25],rock_bass_movement_prob:[8,12],rock_bass_prob:12,role:21,roqb:21,roqba:[],roqba_to_pd_port:21,run:16,runtimeerror:15,sampl:[],sanit:15,satisfactori:16,save:0,save_current_behaviour:0,saved_behaviour:0,scale:[1,8,13,20,22],scale_walk:1,scales_and_harmoni:[],scales_by_frequ:[4,20],scroll:[13,16],scroll_filenam:13,search:[1,6],search_suitable_melodi:25,second:[15,16],select:[1,17],select_next_anchor_tick:1,select_next_harmoni:1,self:[1,9,25],send:[1,4,5,9,14,18],send_cycle_po:5,send_voice_adsr:14,send_voice_pan:14,send_voice_peak_level:14,send_voice_volum:14,sender:[14,18],sendout_offset:1,sent:16,separ:18,seq1:1,seq2:1,sequenc:[],sequence_filenam:13,sequence_length:21,sequence_monitor:13,seri:17,set:[],set_:20,set_binaural_diff:1,set_freq:22,set_met:[1,2,11],set_note_length_group:25,set_pan_po:25,set_rhythm_group:[4,25],set_scal:[1,4],set_slide_msec:14,set_slide_msecs_for_all_voic:14,set_slide_to_0:14,set_stat:[],set_transpos:14,set_wavet:[],setter:[0,25],shell:16,shift_pattern:1,shortest:16,should:[1,3,4,5,15,21],should_play_a_melodi:21,shuffle_delai:[4,21],sin:17,sine:[22,24],sine_control:[],sinesum:17,sinewav:17,singl:[1,4,14,22],size:[15,17],slave:[4,21,25],sleep:4,slide:[8,14,21],slide_duration_msec:21,slide_duration_prop:[8,21],slide_in_msec:[],slow_and_slidi:21,smallest:15,smoothen:3,snapshot:[],snare:3,snd:[],socket:5,some:[4,16],sort:1,sort_import:8,sort_voices_by_import:1,sound:[4,9,14,16],sourc:[0,1,2,3,5,7,9,11,13,14,15,17,18,21,22,25],space:18,special:3,specifi:[0,1,14,15,18,25],speed:[4,9,16,21,25],speed_chang:21,speed_target:21,splash:3,split:17,start:[],start_scal:21,startup:[],state:[1,3,4,14,25],step:[1,4],stop:[2,14,16],stop_all_not:[4,14],stop_notes_of_voic:14,str:17,stream:[1,16],stream_analyz:[1,4],strict_harmoni:20,string:[17,18],style:21,subclass:0,sudo:[],sum:[12,15,17,20,21],sum_:15,suppos:23,synchron:[5,16],system:16,tail:16,take:[4,21],target:[1,9,15,21],tenor:8,tern:15,ternari:8,ternary_group:[8,25],test:[],test_sett:0,testmod:[],thei:22,them:0,thi:[0,1,3,8,9,10,12,14,15,16,21,22],those:[],thread:[1,7,16],tick:[1,21],time:[4,14,22],tmp_length_2_strict:20,to_check:15,to_gui_port:21,todo:[20,21],tom:3,tonal:1,tone_rang:21,too:1,trace_send:18,track:[],track_voices_length:21,transform:15,transit:21,transition_strategi:21,transpos:[4,21],trap:20,trigger:15,tripl:21,tune:[1,3],turn:14,twice:[],txt:[13,16],type:[15,21],ubuntu:[],udp:18,underli:[1,3],unit:[4,15],unmut:14,unpaus:[2,14,16],until:16,updat:5,update_current_microvolum:25,update_gui:5,upon:0,upward:[3,21],usag:9,use_proportional_slide_dur:21,util:[],val:[0,1,3,14],valu:[0,1,3,5,12,14,15,17,22,25],variat:22,variou:8,version:21,vid:[0,14],voic:[],voice_attr:8,voice_behaviour:21,voice_composer_attr:8,voice_get:0,voice_id:14,voice_regist:21,vol:[3,14],volum:14,walk:1,watch:16,wave:22,wavet:[4,14,17,21,25],wavetable_spec:21,weight:[4,11,13,17],well:15,well_formed:15,when:[5,21],where:[],which:[15,16,17,22,25],without:1,would:1,wrapper:[],write:[0,9],write_saved_behaviour:0,write_to_fil:[0,13],xrang:[15,17],you:16,zero:11},titles:["behaviour_dict","composers","director","drummer","Main Call Chains and Sequences","gui_connect","Roqba - a responsive realtime music machine","main","melodic_behaviours","melody_player","meters","metronome","movement_probabilities","notator","note_gateway","note_length_groupings","Overview","pd_wavetables","pdsender","roqba","scales_and_harmonies","settings","sine_controllers","static","utilities","voice"],titleterms:{"abstract":1,"class":1,"static":23,amadinda:1,audio:16,baroq:1,base:1,behaviour_dict:0,call:4,chain:4,command:[],compos:[1,6],depend:16,diagram:16,director:2,document:6,drummer:3,further:[],get:16,gui_connect:5,indic:6,introduct:16,machin:6,main:[4,7],melodic_behaviour:8,melody_play:9,meter:10,metronom:11,movement_prob:12,music:6,notat:13,note_gatewai:14,note_length_group:15,overview:16,pd_wavet:17,pdsender:18,player:6,readm:[],realtim:6,rendezv:1,respons:6,roqba:[6,19],sampl:16,scales_and_harmoni:20,sequenc:4,set:21,sine_control:22,start:16,synthes:6,tabl:6,util:24,voic:25}})