/**
 * @author alexander.farkas
 * 
 * @version 2.5.3
 * project site: http://plugins.jquery.com/project/AjaxManager
 */
(function($){
	$.support.ajax = !!(window.XMLHttpRequest);
	var needActiveXFix = false;
	if(window.ActiveXObject){
		try{
			new ActiveXObject("Microsoft.XMLHTTP");
			$.support.ajax = true;
		} catch(e){
			$.support.ajax = false;
			if(window.XMLHttpRequest){
				$.ajaxSetup({xhr: function(){
					return new XMLHttpRequest();
				}});
				$.support.ajax = true;
			}
		}
	}
	$.manageAjax = (function(){
		var cache 			= {},
			queues			= {},
			presets 		= {},
			activeRequest 	= {},
			allRequests 	= {},
			triggerEndCache = {},
			defaults 		= {
						queue: true, //clear
						maxRequests: 1,
						abortOld: false,
						preventDoubbleRequests: true,
						cacheResponse: false,
						complete: function(){},
						error: function(ahr, status){
							var opts = this;
							if(status && status.indexOf('error') != -1){
								setTimeout(function(){
									var errStr = status +': ';
									if(ahr.status){
										errStr += 'status: '+ ahr.status +' | ';
									}
									errStr += 'URL: '+ opts.url;
									throw new Error(errStr);
								}, 1);
							}
						},
						success: function(){},
						abort: function(){}
				}
		;
		
		function create(name, settings){
			var publicMethods = {};
			presets[name] = presets[name] ||
				{};
			
			$.extend(true, presets[name], $.ajaxSettings, defaults, settings);
			
			if(!allRequests[name]){
				allRequests[name] 	= {};
				activeRequest[name] = {};
				activeRequest[name].queue = [];
				queues[name] 		= [];
				triggerEndCache[name] = [];
			}
			$.each($.manageAjax, function(fnName, fn){
				if($.isFunction(fn) && fnName.indexOf('_') !== 0){
					publicMethods[fnName] = function(param, param2){
						if(param2 && typeof param === 'string'){
							param = param2;
						}
						fn(name, param);
					};
				}
			});
			return publicMethods;
		}
		
		function complete(opts, args){
			
			if(args[1] == 'success' || args[1] == 'notmodified'){
				opts.success.apply(opts, [args[0].successData, args[1]]);
				if (opts.global) {
					$.event.trigger("ajaxSuccess", args);
				}
			}
			
			if(args[1] === 'abort'){
				opts.abort.apply(opts, args);
				if(opts.global){
					$.active--;
					$.event.trigger("ajaxAbort", args);
				}
			}
			
			opts.complete.apply(opts, args);
			
			if (opts.global) {
				$.event.trigger("ajaxComplete", args);
			}
			
			if (opts.global && ! $.active){
				$.event.trigger("ajaxStop");
			}
			//args[0] = null; 
		}
		
		function proxy(oldFn, fn){
			return function(xhr, s, e){
				fn.call(this, xhr, s, e);
				oldFn.call(this, xhr, s, e);
				xhr = null;
				e = null;
			};
		}
		
					
		function callQueueFn(name){
			var q = queues[name];
			if(q && q.length){
				var fn = q.shift();
				if(fn){
					fn();
				}
			}
		}

		
		function add(name, opts){
			if(!presets[name]){
				create(name, opts);
			}
			opts = $.extend({}, presets[name], opts);
			//aliases
			var allR 	= allRequests[name],
				activeR = activeRequest[name],
				queue	= queues[name];
			
			var id 				= opts.type +'_'+ opts.url.replace(/\./g, '_'),
				triggerStart 	= true,
				oldComplete 	= opts.complete,
				ajaxFn 			= function(){
									activeR.queue.push(id);
									activeR[id] = {
										xhr: false,
										ajaxManagerOpts: opts
									};
									activeR[id].xhr = $.ajax(opts);
									return id;
								}
				;
				
			if(opts.data){
				id += (typeof opts.data == 'string') ? opts.data : $.param(opts.data);
			}
			
			if(opts.preventDoubbleRequests && allRequests[name][id]){
				return false;
			}
			
			allR[id] = true;
			
			opts.complete = function(xhr, s, e){
				var triggerEnd = true;
				if(opts.abortOld){
					$.each(activeR.queue, function(i, activeID){
						if(activeID == id){
							return false;
						}
						abort(name, activeID);
						return activeID;
					});
				}
				oldComplete.call(this, xhr, s, e);
				//stop memory leak
				if(activeRequest[name][id]){
					if(activeRequest[name][id] && activeRequest[name][id].xhr){
						activeRequest[name][id].xhr = null;
					} 
					activeRequest[name][id] = null;
				}
				triggerEndCache[name].push({xhr: xhr, status: s});
				xhr = null;
				activeRequest[name].queue = $.grep(activeRequest[name].queue, function(qid){
					return (qid !== id);
				});
				allR[id] = false;
				
				e = null;
				
				delete activeRequest[name][id];
				
				$.each(activeR, function(id, queueRunning){
					if(id !== 'queue' || queueRunning.length){
						triggerEnd = false;
						return false;
					}
				});
				
				if(triggerEnd){
					$.event.trigger(name +'End', [triggerEndCache[name]]);
					$.each(triggerEndCache[name], function(i, cached){
						cached.xhr = null; //memory leak
					});
					triggerEndCache[name] = [];
				}
			};
			
			if(cache[id]){
				ajaxFn = function(){
					activeR.queue.push(id);
					complete(opts, cache[id]);
					return id;
				};
			} else if(opts.cacheResponse){
				 opts.complete = proxy(opts.complete, function(xhr, s){
					if( s !== "success" && s !== "notmodified" ){
						return false;
					}
					cache[id][0].responseXML 	= xhr.responseXML;
					cache[id][0].responseText 	= xhr.responseText;
					cache[id][1] 				= s;
					//stop memory leak
					xhr = null;
					return id; //strict
				});
				
				opts.success = proxy(opts.success, function(data, s){
					cache[id] = [{
						successData: data,
						ajaxManagerOpts: opts
					}, s];
					data = null;
				});
			}
			
			ajaxFn.ajaxID = id;
			
			$.each(activeR, function(id, queueRunning){
				if(id !== 'queue' || queueRunning.length){
					triggerStart = false;
					return false;
				}
			});
			
			if(triggerStart){
				$.event.trigger(name +'Start');
			}
			if(opts.queue){
				opts.complete = proxy(opts.complete, function(){
					
					callQueueFn(name);
				});
				 
				if(opts.queue === 'clear'){
					queue = clear(name);
				}
				
				queue.push(ajaxFn);
				
				if(activeR.queue.length < opts.maxRequests){
					callQueueFn(name); 
				}
				return id;
			}
			
			
			
			return ajaxFn();
		}
		
		function clear(name, shouldAbort){
			$.each(queues[name], function(i, fn){
				allRequests[name][fn.ajaxID] = false;
			});
			queues[name] = [];
			
			if(shouldAbort){
				abort(name);
			}
			return queues[name];
		}
		
		function getXHR(name, id){
			var ar = activeRequest[name];
			if(!ar || !allRequests[name][id]){
				return false;
			}
			if(ar[id]){
				return ar[id].xhr;
			}
			var queue = queues[name],
				xhrFn;
			$.each(queue, function(i, fn){
				if(fn.ajaxID == id){
					xhrFn = [fn, i];
					return false;
				}
				return xhrFn;
			});
			return xhrFn;
		}
		
		function abort(name, id){
			var ar = activeRequest[name];
			if(!ar){
				return false;
			}
			function abortID(qid){
				if(qid !== 'queue' && ar[qid] && ar[qid].xhr){
					try {
						ar[qid].xhr.abort();
					} catch(e){}
					complete(ar[qid].ajaxManagerOpts, [ar[qid].xhr, 'abort']);
				}
				return null;
			}
			if(id){
				return abortID(id);
			}
			return $.each(ar, abortID);
		}
		
		function unload(){
			$.each(presets, function(name){
				clear(name, true);
			});
			cache = {};
		}
		
		return {
			defaults: 		defaults,
			add: 			add,
			create: 		create,
			cache: 			cache,
			abort: 			abort,
			clear: 			clear,
			getXHR: 		getXHR,
			_activeRequest: activeRequest,
			_complete: 		complete,
			_allRequests: 	allRequests,
			_unload: 		unload
		};
	})();
	//stop memory leaks
	$(window).unload($.manageAjax._unload);
})(jQuery);