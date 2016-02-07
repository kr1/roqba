Search.setIndex({envversion:46,filenames:["behaviour_dict","composers","director","drummer","events_and_messages","gui_connect","index","main","melodic_behaviours","melody_player","meters","metronome","movement_probabilities","notator","note_gateway","note_length_groupings","overview","pd_wavetables","pdsender","readme","roqba","scales_and_harmonies","settings","sine_controllers","static","utilities","voice"],objects:{"roqba.composers":{abstract_composer:[1,0,0,"-"],amadinda:[1,0,0,"-"],baroq:[1,0,0,"-"]},"roqba.composers.abstract_composer":{AbstractComposer:[1,4,1,""]},"roqba.composers.abstract_composer.AbstractComposer":{assemble_real_scale:[1,5,1,""],choose_rhythm:[1,1,1,""],generate:[1,1,1,""],generate_real_scale:[1,1,1,""],report:[1,1,1,""],set_binaural_diffs:[1,1,1,""],set_meter:[1,1,1,""],set_scale:[1,1,1,""]},"roqba.composers.amadinda":{Composer:[1,4,1,""]},"roqba.composers.amadinda.Composer":{all_python_words:[1,1,1,""],choose_rhythm:[1,1,1,""],generate:[1,1,1,""],make_new_pattern:[1,1,1,""],next_voice_note:[1,1,1,""],shift_pattern:[1,1,1,""]},"roqba.composers.baroq":{Composer:[1,4,1,""]},"roqba.composers.baroq.Composer":{acceptable_harm_for_length:[1,1,1,""],acceptable_harmony:[1,1,1,""],add_duration_in_msec:[1,1,1,""],apply_scale:[1,1,1,""],choose_rhythm:[1,1,1,""],drum_fill_handler:[1,1,1,""],drum_mark_handler:[1,1,1,""],embellish:[1,1,1,""],flatten_chord:[1,5,1,""],generate:[1,1,1,""],get_deltas:[1,5,1,""],is_base_harmony:[1,1,1,""],ornament_handler:[1,1,1,""],scale_walker:[1,5,1,""],set_binaural_diffs:[1,1,1,""],sort_voices_by_importance:[1,1,1,""],stream_analyzer:[1,1,1,""]},"roqba.director":{Director:[2,4,1,""],random:[2,2,1,""]},"roqba.director.Director":{add_setters:[2,1,1,""],check_incoming_messages:[2,1,1,""],make_length:[2,1,1,""],new_microspeed_sine:[2,1,1,""],new_random_meter:[2,1,1,""],new_speed:[2,1,1,""],pause:[2,1,1,""],set_meter:[2,1,1,""],stop:[2,1,1,""],unpause:[2,1,1,""]},"roqba.drummer":{ContFrame:[3,4,1,""],Drummer:[3,4,1,""],random:[3,2,1,""]},"roqba.drummer.ContFrame":{confirm:[3,3,1,""],ctl2:[3,3,1,""],ctl:[3,3,1,""],meta:[3,3,1,""],pan2:[3,3,1,""],pan:[3,3,1,""],vol:[3,3,1,""]},"roqba.drummer.Drummer":{cont_frame:[3,1,1,""],create_pattern:[3,1,1,""],empty_pattern:[3,1,1,""],generate:[3,1,1,""],high_low_seq:[3,1,1,""],mark_frame:[3,1,1,""],push_value:[3,1,1,""],smoothen:[3,1,1,""]},"roqba.main":{main:[7,2,1,""]},"roqba.metronome":{Metronome:[11,4,1,""]},"roqba.metronome.Metronome":{beat:[11,1,1,""],reset:[11,1,1,""],set_meter:[11,1,1,""]},"roqba.notator":{Notator:[13,4,1,""],main:[13,2,1,""]},"roqba.notator.Notator":{add_note:[13,1,1,""],draw:[13,1,1,""],get_unix_scroll_command:[13,1,1,""],make_matrix:[13,1,1,""],note_to_file:[13,1,1,""],post_process:[13,1,1,""],reset:[13,1,1,""],write_to_file:[13,1,1,""]},"roqba.note_gateway":{NoteGateway:[14,4,1,""]},"roqba.note_gateway.NoteGateway":{drum_hub_gen:[14,1,1,""],hub_gen:[14,1,1,""],mute_voice:[14,1,1,""],pause:[14,1,1,""],pd_send_drum_note:[14,1,1,""],pd_send_duration:[14,1,1,""],pd_send_note:[14,1,1,""],pd_send_wavetable:[14,1,1,""],send_voice_adsr:[14,1,1,""],send_voice_pan:[14,1,1,""],send_voice_peak_level:[14,1,1,""],send_voice_volume:[14,1,1,""],set_slide_msecs:[14,1,1,""],set_slide_msecs_for_all_voices:[14,1,1,""],set_slide_to_0:[14,1,1,""],set_transpose:[14,1,1,""],stop:[14,1,1,""],stop_all_notes:[14,1,1,""],stop_notes_of_voice:[14,1,1,""],unpause:[14,1,1,""]},"roqba.static":{"__init__":[24,0,0,"-"],melodic_behaviours:[8,0,0,"-"],meters:[10,0,0,"-"],movement_probabilities:[12,0,0,"-"],note_length_groupings:[15,0,0,"-"],scales_and_harmonies:[21,0,0,"-"],settings:[22,0,0,"-"]},"roqba.static.note_length_groupings":{analyze_grouping:[15,2,1,""],assemble:[15,2,1,""],badly_formeD:[15,2,1,""],cut_grouping_to_size:[15,2,1,""],get_grouping:[15,2,1,""]},"roqba.utilities":{"__init__":[25,0,0,"-"],behaviour_dict:[0,0,0,"-"],gui_connect:[5,0,0,"-"],melody_player:[9,0,0,"-"],pd_wavetables:[17,0,0,"-"],pdsender:[18,0,0,"-"],sine_controllers:[23,0,0,"-"]},"roqba.utilities.behaviour_dict":{BehaviourDict:[0,4,1,""],test_setter:[0,2,1,""]},"roqba.utilities.behaviour_dict.BehaviourDict":{read_or_create_saved_behaviours:[0,1,1,""],save_current_behaviour:[0,1,1,""],voice_get:[0,1,1,""],write_saved_behaviours:[0,1,1,""]},"roqba.utilities.gui_connect":{GuiConnect:[5,4,1,""]},"roqba.utilities.gui_connect.GuiConnect":{handle_caesura:[5,1,1,""],read_incoming_messages:[5,1,1,""],send:[5,1,1,""],send_cycle_pos:[5,1,1,""],update_gui:[5,1,1,""]},"roqba.utilities.melody_player":{MelodyPlayer:[9,4,1,""],extract_modified_move:[9,2,1,""]},"roqba.utilities.melody_player.MelodyPlayer":{play:[9,1,1,""]},"roqba.utilities.pd_wavetables":{harmonic_wavetable:[17,2,1,""],random_harmonic_wavetable:[17,2,1,""],random_wavetable:[17,2,1,""]},"roqba.utilities.pdsender":{PdSender:[18,4,1,""],Sender:[18,4,1,""]},"roqba.utilities.pdsender.PdSender":{format_msg_list:[18,5,1,""],send:[18,1,1,""]},"roqba.utilities.pdsender.Sender":{trace_send:[18,1,1,""]},"roqba.utilities.sine_controllers":{MultiSine:[23,4,1,""],Sine:[23,4,1,""]},"roqba.utilities.sine_controllers.MultiSine":{assemble_funnel:[23,1,1,""],get_value:[23,1,1,""],get_value_as_factor:[23,1,1,""],set_freqs:[23,1,1,""]},"roqba.utilities.sine_controllers.Sine":{get_value:[23,1,1,""],set_freq:[23,1,1,""]},"roqba.voice":{Voice:[26,4,1,""]},"roqba.voice.Voice":{add_setters_for_behaviour_dict:[26,1,1,""],apply_overhanging_notes:[26,1,1,""],exceeds:[26,1,1,""],in_the_middle:[26,1,1,""],make_wavetable:[26,1,1,""],manage_melody_note:[26,1,1,""],new_microvolume_sine:[26,1,1,""],next_note:[26,1,1,""],register_other_voices:[26,1,1,""],reload_register:[26,1,1,""],reset_slave:[26,1,1,""],search_suitable_melody:[26,1,1,""],set_pan_pos:[26,1,1,""],set_rhythm_grouping:[26,1,1,""],set_state:[26,1,1,""],update_current_microvolume:[26,1,1,""],voice:[26,1,1,""]},roqba:{"__init__":[20,0,0,"-"],director:[2,0,0,"-"],drummer:[3,0,0,"-"],main:[7,0,0,"-"],metronome:[11,0,0,"-"],notator:[13,0,0,"-"],note_gateway:[14,0,0,"-"],voice:[26,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","method","Python method"],"2":["py","function","Python function"],"3":["py","attribute","Python attribute"],"4":["py","class","Python class"],"5":["py","staticmethod","Python static method"]},objtypes:{"0":"py:module","1":"py:method","2":"py:function","3":"py:attribute","4":"py:class","5":"py:staticmethod"},terms:{"1x1":15,"1x2":15,"1x3":15,"1x4":15,"1x5":15,"1x6":15,"1x7":15,"1x8":15,"2x1":15,"2x2":15,"2x3":15,"3x1":15,"3x2":15,"4x1":15,"4x2":15,"5x1":15,"6th":12,"6x1":15,"8th":12,"8x1":15,"__assembl":17,"__main__":[8,12,15,21,22],"__name__":[8,12,15,21,22],"__setitem__":0,"_composers_":16,"_plai":[4,16],"abstract":17,"break":15,"case":15,"class":[0,2,3,5,9,11,13,14,18,23,26],"default":[0,8,15],"final":16,"function":[1,3,14,15,17,23],"import":[1,8,12,15,17,19,21,22],"int":[5,15,26],"new":[1,4,14,15,23,26],"return":[0,1,4,11,15,17,23,26],"static":[],"true":[0,8,15,22,23,26],abstract_compos:1,abstractcompos:1,acceptable_harm_for_length:1,acceptable_harmoni:1,accord:[1,14,26],action:1,activ:14,add:[0,1],add_duration_in_msec:1,add_not:13,add_sett:2,add_setters_for_behaviour_dict:26,add_voic:[],adjust:19,adsr:[14,22],after:[],again:14,alia:3,all:[3,14,15,17,22],all_python_word:1,all_strict_harmoni:21,allow:3,also:[1,16,26],alt:22,alto:8,amadinda:22,amplitud:17,analys:1,analyz:16,analyze_group:15,ani:[1,23],anoth:4,app:[16,19,26],append:[3,15],appli:[10,26],applic:7,apply_overhanging_not:[4,26],apply_scal:[1,4],area:26,arg:0,around:23,arrai:[1,17],assembl:[3,15,17,23,26],assemble_funnel:23,assemble_real_scal:1,assert:15,attribut:[1,4,8,9,26],audiobuf:[],autom:4,automate_adsr:22,automate_binaural_diff:22,automate_met:22,automate_microspeed_chang:22,automate_microvolume_chang:22,automate_note_duration_min_max:22,automate_note_duration_prop:22,automate_num_parti:22,automate_pan:22,automate_scal:22,automate_slid:22,automate_speed_chang:22,automate_transpos:22,automate_wavet:22,autonom:22,averag:22,back:26,background:[],badli:15,badly_form:15,baroq:[],base:12,base_harmoni:21,basic:4,bass:[3,8,22,26],bass_movement_prob:[8,12],bass_prob:12,beat:[4,5,11,15],been:0,befor:0,behaviour:[0,1,2,14,16,22,26],behaviourdict:[0,22],belong:26,between:[1,22],binari:15,binaur:[4,22],binaural_diff:22,bit:26,block:14,both:16,bounc:26,bound:1,buffer_length:13,bulgarian:22,bypass:14,caesura:[4,5,16],caesura_prob:22,calcul:[23,26],call:[],can:[1,9,19,22],capabl:17,cat:19,ceasura:16,center:26,chang:[1,3],change_mast:26,change_rhythm_after_tim:8,check:[0,1,2,15,16,22],check_incoming_messag:[2,4],choic:4,choos:1,choose_rhythm:[1,4],chord:1,chosen:[1,26],clock:16,code:1,coeffici:26,combin:[15,23],come:[],command:[],comment:4,common:26,common_adsr:22,common_binaural_diff:22,common_note_dur:22,common_wavet:22,commun:14,complet:5,compli:4,concern:14,condit:16,configur:1,confirm:3,consecut:17,consid:[],consist:3,constant:[10,15],constraint:22,cont:3,cont_fram:3,contain:[10,12,14,16,24,25],content:6,context:1,contfram:3,continu:[3,19],control:[14,16,23,25,26],coroutin:[4,16],counter:11,crash:3,creat:[0,1,3,4,8,9,17,21,22,26],create_pattern:3,creation:3,creb:[],ctl2:3,ctl:[3,14],cumul:4,current:[0,1,11,26],custom:[0,25],cut:15,cut_grouping_to_s:15,cycle_po:[4,13],cymbal:3,data:[13,19,24],datagram:18,dataobject:[],decis:4,def:[15,17],default_behaviour:22,default_embellishment_prob:22,default_fast_group:15,default_group:8,default_meter_length:15,default_movement_prob:[8,12],default_note_duration_prop:22,default_note_length_group:15,default_num_parti:22,default_pan_posit:22,default_pause_prob:22,default_prob:12,default_slower_group:15,default_ternary_group:15,default_volum:22,defin:[0,3,9],deken:19,delta:[1,26],densiti:3,depend:[],destroi:14,det:17,determin:17,diagram:[],diaton:[1,8,21],dict:[0,3,5,25],dictionari:0,diff:[4,15,22],dir:1,direct:[1,26],disharm:21,doctest:15,draw:13,drum:[1,3,4,14,16],drum_fil:12,drum_fill_handl:1,drum_hub:[],drum_hub_gen:14,drum_mark_handl:1,drummer:[],dual:22,duplic:3,durat:[1,4,14,22],dure:[15,24],dynam:21,each:[1,4,17],eadsr:[],either:1,elaps:23,els:15,embellish:[1,4,16,26],embellishment_prob:8,embellishment_speed_lim:22,empti:3,empty_pattern:3,encod:5,engin:[4,9,14],entri:15,environ:8,equal:[15,23],equal_pow:23,etc:[3,25,26],even:[17,22],eventu:[4,26],everi:[0,5,15],exampl:19,exce:26,execut:24,exist:15,expect:17,experiment:21,extend:[1,12],extern:19,extract_modified_mov:9,fallback:[3,15],fals:[15,22,26],fast:[1,22],fast_group:8,field:3,file:[0,9,19,22],fill:[1,16],filter:15,first:[1,15,22],flag:[1,16],flat_mid:[8,22],flat_mid_movement_prob:[8,12],flat_mid_prob:12,flatspac:[],flatten_chord:1,flow:14,folder:19,follow:[4,16,19,21,26],form:15,format:[3,15,18],format_msg_list:18,found:15,frame:[3,4,16],freq:23,frequenc:23,from:[1,3,8,12,14,19,22],from_gui_port:22,fun:17,further:[],gate:15,gatewai:[1,2,4,16,26],gener:[1,3,4,14,16,26],generate_real_scal:1,get:[],get_delta:1,get_group:15,get_unix_scroll_command:13,get_valu:23,get_value_as_factor:23,given:[0,1,3,9,14,15,16,17,22,23],gpan:[],graphic:19,group:[1,8,15,22,26],gui:[5,22],gui_host:22,guiconnect:5,half_beat:22,handl:1,handle_caesura:5,handle_incoming_messag:[],happen:5,harm:1,harmon:[1,4,16,17,21,22],harmoni:[1,4,21,24],harmonic_interv:21,harmonic_wavet:17,hat:3,have:[1,4,17],hear:9,heavi:[4,8,15],heavy_group:8,helper:17,here:[1,26],hertz:1,high:[3,8,22,26],high_low_seq:3,highest_note_num:22,hold:8,host:18,html:[],hub:4,hub_gen:14,human:10,imp:1,implement:15,implic:15,in_the_middl:26,incom:[2,5,18,26],index:6,info:1,initi:3,instal:19,instanc:[1,9],interfac:[],intern:11,interv:[1,2,3],introduct:[],ipython:19,is_base_harmoni:1,item:15,itertool:[12,21],join:17,json:5,keep:22,kei:[0,3,5,12,15,22],kernel:[],keyerror:15,known:[],kwarg:0,lambda:[15,17],last:15,later:4,lead:8,leap:22,legato_prob:8,length:[1,15,19,26],let:14,librari:19,like:24,limit:26,list:[12,17,18,21,22,23],load:15,local:22,local_set:22,localhost:22,log:19,loop:[3,16],low:3,lowest_note_num:22,made:4,main:[],mainli:0,major:1,make_length:2,make_matrix:13,make_new_pattern:1,make_wavet:26,manage_melody_not:26,manual:[],map:[1,17],mark:[1,3],mark_fram:3,marker:[1,3],master:26,mat:13,max:[1,26],max_adsr:22,max_binaural_diff:22,max_num_parti:22,max_shuffl:[10,22],max_spe:22,maximum:17,mean:22,melod:[8,14,21],melodi:[3,9,12,22,26],melodic_behaviour:[],melody_set:8,melodyplay:9,messag:[2,5,9,14,17,18,19],meta:3,meter:[],meter_length:15,meter_po:[1,26],method:[0,1,3,4,14,16,23,26],metronom:[],microspeed_max_speed_in_hz:22,microspeed_vari:22,microvolume_max_speed_in_hz:22,microvolume_vari:22,mid:[8,22,26],mid_prob:12,middl:22,middle_voices_movement_prob:[8,12],millisec:14,millisecond:1,min:[1,26],min_adsr:22,min_spe:22,minor:1,mode:[15,26],modifi:[0,1,16,26],modprob:[],modul:[0,6,8,10,12,15,16,23,24,25],moment:23,motex:[],move:[4,9,26],movement:[8,24,26],movement_prob:[],msec:[14,22],msg:[5,14,18],multipl:23,multisin:23,must:23,mute:14,mute_voic:14,name:[0,1,8,22,26],necess:4,necessari:[9,15,19],need:19,neg:15,new_microspeed_sin:2,new_microvolume_sin:26,new_random_met:[2,4],new_spe:2,next:[1,4,26],next_not:26,next_voice_not:1,nin:15,noadc:[],non:15,none:[0,1,2,3,15,22,26],normal:4,notat:[],note:[1,4,13,14,15,16,19,22,23,26],note_delta:1,note_duration_prop:4,note_gatewai:[],note_length_group:[],note_rang:26,note_to_fil:[4,13],notegatewai:14,notes_per_scal:21,num_lin:13,num_ton:22,num_voic:13,number:[3,17,23],number_of_tones_in_3rd_voic:22,number_of_voic:22,object:[14,19,23],obtain:16,octav:1,octave_offset:22,odd:[15,17,22],off:[14,26],offset:1,on_off_pattern:26,onli:24,open:19,origin:23,ornament:[1,12],ornament_handl:1,oscil:23,oss:[],other:[15,26],other_voic:[],otherwis:[0,26],out:14,over:[1,5,22],overhang:26,overlaid:23,overridden:22,overview:[],padsp:[],page:6,pan2:3,pan:[3,4,14,22],pan_controls_binaural_diff:22,pan_po:26,param:26,part:17,partial:17,particular:[],patt:3,pattern:[3,15,26],paus:[2,14,15,19],pause_prob:8,pcm:[],pd_host:22,pd_port:22,pd_send_drum_not:14,pd_send_dur:14,pd_send_not:14,pd_send_wavet:14,pd_wavet:[],pdsender:[],peak_level:14,penta:8,penta_minor:[8,21],pentaton:21,per_voic:22,percussion_hub:4,perform:16,permut:[12,21],pitch:26,place:4,plai:[9,19],plugin:19,polyphon:[1,4],pop:15,port:18,posit:[4,5],possibl:22,post:3,post_process:13,pprint:15,predominantli:22,prepend:[],present:[0,14],present_not:1,prevail:22,print:[1,8,12,15,21,22],privid:15,probabl:[12,24,26],process:[],produc:[1,23],product:[14,19],prop:4,proport:22,provid:23,pure:19,puredata:[14,17,19],purpos:14,push_valu:3,python:19,quarter:22,queue:2,rais:15,random:[1,2,3,17,22,26],random_harmon:22,random_harmonic_wavet:17,random_wavet:17,randomli:[1,17],rang:[1,8,22,23,26],raw:5,read:[0,5,24,26],read_incoming_messag:5,read_or_create_saved_behaviour:0,readm:[],real:1,real_not:26,real_scal:9,reappli:26,recommend:19,reconsid:15,regist:[0,1,4,8,26],register_other_voic:26,relat:[3,22,26],reli:19,reload:26,reload_regist:[1,26],repeat:19,report:1,repres:17,represent:19,requir:15,reset:[4,11,13,26],reset_slav:26,result:16,resum:19,retriev:26,rhythm:[1,15],rhythmic:26,ride:3,rock:22,rock_bass:[8,22,26],rock_bass_movement_prob:[8,12],rock_bass_prob:12,roqb:22,roqba:[],run:[16,19],runtimeerror:15,sanit:15,satisfactori:16,save:0,save_current_behaviour:0,saved_behaviour:0,scale:[1,8,21,23],scale_walk:1,scales_and_harmoni:[],scales_by_frequ:[4,21],scroll:[13,19],scroll_filenam:13,search:[1,6],search_suitable_melodi:26,second:[15,19],select:17,self:[1,9],send:[1,4,5,9,14,18],send_cycle_po:5,send_voice_adsr:14,send_voice_pan:14,send_voice_peak_level:14,send_voice_volum:14,sender:[14,18],sent:16,separ:18,seq1:1,seq2:1,sequenc:[],seri:17,set:[],set_:21,set_binaural_diff:1,set_freq:23,set_met:[1,2,11],set_pan_po:26,set_rhythm_group:[4,26],set_scal:[1,4],set_slide_msec:14,set_slide_msecs_for_all_voic:14,set_slide_to_0:14,set_stat:26,set_transpos:14,set_wavet:[],setter:[0,26],shell:19,shift_pattern:1,shortest:19,should:[3,4,5,15],should_play_a_melodi:22,shuffle_delai:[4,22],sine:[23,25],sine_control:[],sinesum:17,sinewav:17,singl:[1,4,14,23],size:15,slave:[4,22,26],sleep:4,slide:[8,14,22],slide_duration_msec:22,slide_duration_prop:[8,22],slide_in_msec:[],smallest:15,smoothen:3,snapshot:[],snare:3,snd:[],socket:5,some:[4,19],sort:1,sort_import:8,sort_voices_by_import:1,sound:[4,9,14,19],sourc:[0,1,2,3,5,7,9,11,13,14,15,17,18,23,26],space:18,special:3,specifi:[0,1,14,15,18,26],speed:[4,9,19,22,26],speed_chang:22,speed_target:22,splash:3,start:[],startup:[],state:[1,3,4,14,26],step:[1,4],stop:[2,14,19],stop_all_not:[4,14],stop_notes_of_voic:14,str:17,stream:[1,16],stream_analyz:[1,4],strict_harmoni:21,string:18,style:22,subclass:0,sudo:[],sum:[12,15,21,22],sum_:15,suppos:24,synchron:[5,16],system:19,tail:19,take:4,target:[1,9,15,22],tenor:8,tern:15,ternari:8,ternary_group:8,test:15,test_sett:0,testmod:15,thei:23,them:0,thi:[0,1,3,8,9,10,12,14,15,19,22,23],those:[],thread:[1,7,16],time:[4,14,23],tmp_length_2_strict:21,to_check:15,to_gui_port:22,todo:[21,22],tom:3,tonal:1,tone_rang:22,too:1,trace_send:18,track:[],track_voices_length:22,transform:15,transit:22,transpos:[4,22],trap:21,trigger:15,tripl:22,tune:[1,3],turn:14,twice:[],txt:[13,19],type:[15,22],ubuntu:[],udp:18,underli:3,unit:[4,15],unmut:14,unpaus:[2,14,19],until:16,updat:[5,22],update_current_microvolum:26,update_gui:5,upon:0,upward:3,usag:9,use_proportional_slide_dur:22,util:[],val:[0,1,2,3,14],valu:[0,1,3,5,12,14,15,17,23,26],variat:[23,26],variou:8,version:22,vid:[0,14],voic:[],voice_attr:8,voice_behaviour:22,voice_composer_attr:8,voice_get:0,voice_id:14,voice_regist:22,vol:[3,14],volum:14,walk:1,watch:19,wave:23,wavet:[4,14,22,26],wavetable_spec:22,weight:[4,11,13],well:15,well_formed:15,when:5,where:[],which:[15,16,17,23,26],without:1,would:1,wrapper:[],write:[0,9],write_saved_behaviour:0,write_to_fil:[0,13],xrang:[15,17],you:19,zero:11},titles:["behaviour_dict","composers","director","drummer","Main Call Chains and Sequences","gui_connect","Roqba - a responsive realtime music machine","main","melodic_behaviours","melody_player","meters","metronome","movement_probabilities","notator","note_gateway","note_length_groupings","Overview","pd_wavetables","pdsender","README","roqba","scales_and_harmonies","settings","sine_controllers","static","utilities","voice"],titleterms:{"abstract":1,"class":1,"static":24,amadinda:1,baroq:1,base:1,behaviour_dict:0,call:4,chain:4,command:[],compos:[1,6],depend:19,diagram:16,director:2,document:6,drummer:3,further:[],get:19,gui_connect:5,indic:6,introduct:16,machin:6,main:[4,7],melodic_behaviour:8,melody_play:9,meter:10,metronom:11,movement_prob:12,music:6,notat:13,note_gatewai:14,note_length_group:15,overview:16,pd_wavet:17,pdsender:18,player:6,readm:19,realtim:6,respons:6,roqba:[6,20],scales_and_harmoni:21,sequenc:4,set:22,sine_control:23,start:19,synthes:6,tabl:6,util:25,voic:26}})