package com.warmer.kgmaker.controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.csvreader.CsvWriter;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.warmer.kgmaker.config.WebAppConfig;
import com.warmer.kgmaker.entity.QAEntityItem;
import com.warmer.kgmaker.query.GraphQuery;
import com.warmer.kgmaker.service.IKGGraphService;
import com.warmer.kgmaker.service.IKnowledgegraphService;
import com.warmer.kgmaker.util.*;
import org.apache.commons.lang3.StringUtils;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import sun.text.normalizer.UCharacter;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.lang.reflect.Array;
import java.nio.charset.Charset;
import java.util.*;
import java.util.regex.Pattern;

@Controller
@RequestMapping(value = "/")
public class KGManagerController extends BaseController {
	@Autowired
	private Neo4jUtil neo4jUtil;
	@Autowired
	private WebAppConfig config;
	@Autowired
	private IKGGraphService KGGraphService;
	@Autowired
	private IKnowledgegraphService kgservice;

	@GetMapping("/")
	public String home(Model model) {
		return "kg/home";
	}
	@GetMapping("/kg/index")
	public String index(Model model) {
		return "kg/index";
	}
	@GetMapping("/kg/test")
	public String test(Model model) {
		return "kg/test";
	}
	@ResponseBody
	@RequestMapping(value = "/getgraph") // call db.labels
	public R<GraphPageRecord<Map<String, Object>>> getgraph(GraphQuery queryItem) {
		R<GraphPageRecord<Map<String, Object>>> result = new R<GraphPageRecord<Map<String, Object>>>();
		GraphPageRecord<Map<String, Object>> resultRecord = new GraphPageRecord<Map<String, Object>>();
		try {
			String name = "tc";
			PageHelper.startPage(queryItem.getPageIndex(), queryItem.getPageSize(), true);
			List<Map<String, Object>> domainList = kgservice.getDomainList(queryItem.getDomain(), name);
			PageInfo<Map<String, Object>> pageInfo = new PageInfo<Map<String, Object>>(domainList);
			long total = pageInfo.getTotal();
			resultRecord.setPageIndex(queryItem.getPageIndex());
			resultRecord.setPageSize(queryItem.getPageSize());
			resultRecord.setTotalCount(new Long(total).intValue());
			resultRecord.setNodeList(pageInfo.getList());
			result.code = 200;
			result.setData(resultRecord);
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}

		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/getdomaingraph")
	public R<HashMap<String, Object>> getDomainGraph(GraphQuery query) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		try {
			HashMap<String, Object> graphData = KGGraphService.getdomaingraph(query);
			result.code = 200;
			result.data = graphData;

		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@CrossOrigin
	@ResponseBody
	@RequestMapping(value = "/getcypherresult")
	public R<HashMap<String, Object>> getcypherresult(String cypher) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		String error="";
		try {
			HashMap<String, Object> graphData = neo4jUtil.GetGraphNodeAndShip(cypher);
			result.code = 200;
			result.data = graphData;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			error=e.getMessage();
			result.setMsg("服务器错误");
		}
		finally {
			if(StringUtil.isNotBlank(error)){
				result.code = 500;
				result.setMsg(error);
			}
		}
		return result;
	}
	@CrossOrigin
	@ResponseBody
	@RequestMapping(value = "/getEntityIndex")
	public R<ArrayList<HashMap<String, Object>>> getEntityIndex(String txt) {
		R<ArrayList<HashMap<String, Object>>> result = new R<ArrayList<HashMap<String, Object>>>();
		//html标签判断标志 true:html标签内容  false：不是html标签内容
		Stack<Character> index_flag = new Stack<Character>();
		//保存分词后的word信息
		LinkedList<HashMap<String,Object>> cut_list = new LinkedList<HashMap<String,Object>>();
		txt = txt.trim().toLowerCase();
		//html标签内容
		String html_index = "";
		//判定是否在code标签内
		Boolean code_flag = false;
		//每个字符匹配正则表达式
		String regex = "([0-9]|[a-z]|\\.|\\-|_)";
		//命令参数
		HashMap<String,String> param_map = new HashMap<>();
		//命令参数窗口
		int comd_window = 3;
		HashMap<String,Object> temp_pair = new HashMap<String,Object>();
		try {
			ArrayList<HashMap<String, Object>> list = new ArrayList<HashMap<String,Object>>();
			for(int i = 0,j = i; i < txt.length() && j<txt.length();i ++){

				if(txt.charAt(i) == '<'){
					html_index = "";
					index_flag.push(txt.charAt(i));
					continue;
				}else if(txt.charAt(i) == '>'){
					index_flag.pop();
					if(!(html_index.equals("code") || html_index.equals("/code")))
						html_index = "";
					continue;
				}else if(!index_flag.isEmpty()){
					html_index = html_index + txt.charAt(i);
					continue;}
				if(html_index.equals("code")){
					code_flag = true;

				}else if(html_index.equals("/code")){
					code_flag = false;
					html_index = "";
				}else{
					code_flag = false;
					html_index = "";
				}
				boolean flag = Pattern.matches(regex, txt.charAt(i)+"");
				if(!flag){continue;}
				int start = i;
				for(j = i+1;j < txt.length();j ++){
					boolean flag2 = Pattern.matches(regex, txt.charAt(j)+"");
					if(!flag2){
						int end = j;
						i = j-1;
						String ent = txt.substring(start,end);
						HashMap<String,Object> word = new HashMap<String,Object>();
						word.put("name",ent);
						word.put("start",start);
						word.put("end",end);
						word.put("code_flag",code_flag);
						//保存实体类别：“命令”，“参数”，"配置文件"，“null”
						word.put("label",null);
						cut_list.add(word);
						break;
					}
				}
			}

			for(int k = 0;k < cut_list.size(); k ++){
				HashMap<String,Object> word = cut_list.get(k);
				String ent = word.get("name").toString();
				boolean code_flag2 = (boolean)word.get("code_flag");
				String start = word.get("start").toString();
				String end = word.get("end").toString();
				String cypher = "";
				if(code_flag2) {//在code标签内
					if(comd_window > 0){
						comd_window --;
						if(!param_map.isEmpty()){
							if(param_map.get(ent) != null){
								HashMap<String,Object> pair = new HashMap<String,Object>();
								pair.put("start",start);
								pair.put("end",end);
								String name = temp_pair.get("name").toString();
								String index = temp_pair.get("index").toString();
								pair.put("name",name);
								pair.put("index",index);
								word.put("label","参数");//更新单词中的label
								list.add(pair);
								continue;
							}
						}
					}
					cypher = "match(n) where (n:`命令` or n:`参数` or n:`配置文件`) and n.name='" + ent + "'  return n";
				}else{//不在code标签内
					if(k != 0){
						String key2 = cut_list.get(k-1).get("name").toString();
						if(key2.equals("use")){
							cypher = "match(n) where (n:`命令`) and n.name='" + ent + "'  return n";
						}else{
							cypher = "match(n) where (n:`参数` or n:`配置文件`) and n.name='" + ent + "'  return n";
						}
					}else {
						cypher = "match(n) where (n:`参数` or n:`配置文件`) and n.name='" + ent + "'  return n";
					}
				}
				HashMap<String, Object> data1 = neo4jUtil.GetGraphNodeAndShip(cypher);
				if(!data1.isEmpty()){
					HashMap<String,Object> pair = new HashMap<String,Object>();
					pair.put("start",start);
					pair.put("end",end);
					pair.put("name",ent);
					ArrayList<HashMap<String,Object>> list2 = (ArrayList<HashMap<String,Object>>)data1.get("node");
					String index = list2.get(0).get("uuid").toString();
					String type = list2.get(0).get("label").toString();
					pair.put("index",index);
					word.put("label",type);//更新单词中的label
					if(type.equals("命令")){
						param_map.clear();
						if(list2.get(0).get("parameter") != null) {
							String params = list2.get(0).get("parameter").toString();
							comd_window = 3;
							temp_pair = pair;
							if (params.trim() != "") {
								String[] param_arr = params.split("\\|\\|\\|");
								for (int i = 0; i < param_arr.length; i++) {
									if(param_arr[i].trim().equals(""))
										continue;
									String[] param_pair = param_arr[i].split(":", 2);
									param_map.put(param_pair[0].trim(), param_pair[1].trim());
								}
							}
						}
					}

					//System.out.print(data1);
					list.add(pair);
				}else{
					HashMap<String,Object> temp2 = new HashMap<>();
					temp2.put(ent,null);
				}
			}

			result.code = 200;
			result.data = list;

		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@CrossOrigin
	@ResponseBody
	@RequestMapping(value = "/getEntityByName")
	public R<HashMap<String, Object>> getEntityByName(String name) {
		name = name.trim().toLowerCase();
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		String error="";
		try {
			String cypher = "match(n) where (n:`命令` or n:`参数` or n:`配置文件`) and n.name='"+name+"'  return n";
			HashMap<String, Object> graphData = neo4jUtil.GetGraphNodeAndShip(cypher);
			ArrayList<HashMap<String,Object>> list = (ArrayList<HashMap<String,Object>>)graphData.get("node");
			//遍历查询到的每个知识
			for(int i = 0; i < list.size(); i ++){
				HashMap<String,Object> node = list.get(i);
				Object label = node.get("label");
				if(label.equals("命令")){
					Object param = node.get("parameter");
					//System.out.println(param);
					if(param != null){
						String[] params = param.toString().split("\\|\\|\\|");
						ArrayList<HashMap<String,String>> param_list = new ArrayList<HashMap<String,String>>();
						//遍历每一条参数
						for(int j = 0; j < params.length; j ++){
							if(!params[j].trim().equals("")){
								String[] pair = params[j].split(":",2);
								HashMap<String,String> param_map = new HashMap<String,String>();
								param_map.put("name",pair[0]);
								param_map.put("value",pair[1]);
								param_list.add(param_map);
							}
						}
						node.put("parameter",param_list);
					}
				}else if(label.equals("配置文件")){
					String config_cypher = "MATCH (n:`配置文件`)-[r]->(m:`参数`) where n.name='"+name+"' RETURN m";
					HashMap<String, Object> config_param = neo4jUtil.GetGraphNodeAndShip(config_cypher);
					ArrayList<HashMap<String,Object>> param_list = (ArrayList<HashMap<String,Object>>)config_param.get("node");
					ArrayList<HashMap<String,String>> config_param_list = new ArrayList<HashMap<String,String>>();
					for(int k = 0; k < param_list.size(); k ++){
						HashMap<String,String> pair = new HashMap<>();
						pair.put("name",param_list.get(k).get("name").toString());
						pair.put("value",param_list.get(k).get("detail").toString().replace("\n\t",""));
						config_param_list.add(pair);
					}
					node.put("parameter",config_param_list);
				}else if(label.equals("参数")){
					ArrayList<HashMap<String,String>> param_list = new ArrayList<HashMap<String,String>>();
					HashMap<String,String> pair = new HashMap<String,String>();
					pair.put("name",node.get("name").toString());
					pair.put("detail",node.get("detail").toString().replace("\n\t",""));
					param_list.add(pair);
					node.put("parameter",param_list);
				}

			}
			result.code = 200;
			result.data = graphData;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			error=e.getMessage();
			result.setMsg("服务器错误");
		}
		finally {
			if(StringUtil.isNotBlank(error)){
				result.code = 500;
				result.setMsg(error);
			}
		}
		return result;
	}

	@CrossOrigin
	@ResponseBody
	@RequestMapping(value = "/getenitiy")
	public R<HashMap<String, Object>> getenitiy(String txt) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		String error="";
		List<String> ss = new ArrayList<String>();
		try {
			txt = txt.trim().toLowerCase();
			txt = txt.replace(". "," ").replace(", "," ")
					.replace("? "," ").replace("! "," ")
					.replace("; "," ").replace(".\r\n"," ")
					.replace("?\r\n"," ").replace(".\r\n"," ")
			.replace("'"," ").replace("\""," ");
//			System.out.println(txt);
			String[] list = txt.split(" ");

			HashMap<String, Object> res = new HashMap<>();


			String temp="";
			List res_list = new ArrayList();
			int end_temp = 0;
			String pattern = "([a-z]|/.)*";
			for(int i = 0; i < list.length; i ++){
				boolean isMatch = Pattern.matches(pattern, list[i]);
				if(!isMatch){
					continue;
				}

				temp = "";
				for( int j = i; j < list.length; j ++){
					if(list[j].trim() == "")
						continue;
					boolean isMatch2 = Pattern.matches(pattern, list[j]);
					if(!isMatch2){
						end_temp = j-1;
						break;
					}
					temp = temp + " " +list[j].trim();
					String cypher1 = "match (n) where n.name=~'"+temp.trim()+".*' return n";
					HashMap<String, Object> data1 = neo4jUtil.GetGraphNodeAndShip(cypher1);
					if(j == list.length - 1){
						end_temp = j;
						break;
					}
					if(data1.isEmpty() && i == j){
						end_temp = i-1;
						break;
					}else if(data1.isEmpty()){
						end_temp = j;
						break;
					}
				}

				String temp2 = "";
				while(end_temp >= i) {
					for (int k = i; k <=end_temp; k++) {
						temp2 = temp2+" "+list[k].trim();
					}
					if(ss.contains(temp2)){
						temp2="";
						end_temp --;
						continue;
					}
					ss.add(temp2);
					String cypher2 = "match (n) where n.name='" + temp2.trim() + "' return n";
					HashMap<String, Object> data2 = neo4jUtil.GetGraphNodeAndShip(cypher2);
					if(!data2.isEmpty()){
						Iterator it=data2.keySet().iterator();
						while(it.hasNext()){
							String key;
							List value = null;
							key=it.next().toString();
							if(key == "node") {
								value = (ArrayList) data2.get(key);
								res_list.addAll(value);
							}
						}
						i = end_temp;
						break;
					}
					temp2 = "";
					end_temp --;
				}
			}

			res.put("node",res_list);
			result.code = 200;
			result.data = res;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			error=e.getMessage();
			result.setMsg("服务器错误");
		}
		finally {
			if(StringUtil.isNotBlank(error)){
				result.code = 500;
				result.setMsg(error);
			}
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/getrelationnodecount")
	public R<String> getrelationnodecount(String domain, long nodeid) {
		R<String> result = new R<String>();
		try {
			long totalcount = 0;
			if (!StringUtil.isBlank(domain)) {
				totalcount = KGGraphService.getrelationnodecount(domain, nodeid);
				result.code = 200;
				result.setData(String.valueOf(totalcount));
			}
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/createdomain")
	public R<String> createdomain(String domain) {
		R<String> result = new R<String>();
		try {
			if (!StringUtil.isBlank(domain)) {
				List<Map<String, Object>> domainItem = kgservice.getDomainByName(domain);
				if (domainItem.size() > 0) {
					result.code = 300;
					result.setMsg("领域已存在");
				} else {
					String name = "tc";
					Map<String, Object> maps = new HashMap<String, Object>();
					maps.put("name", domain);
					maps.put("nodecount", 1);
					maps.put("shipcount", 0);
					maps.put("status", 1);
					maps.put("createuser", name);
					kgservice.saveDomain(maps);// 保存到mysql
					KGGraphService.createdomain(domain);// 保存到图数据
					result.code = 200;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@CrossOrigin
	@ResponseBody
	@RequestMapping(value = "/getmorerelationnode")
	public R<HashMap<String, Object>> getmorerelationnode(String domain, String nodeid) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		try {
			if (!StringUtil.isBlank(domain)) {
				HashMap<String, Object> graphModel = KGGraphService.getmorerelationnode(domain, nodeid);
				if (graphModel != null) {
					result.code = 200;
					result.setData(graphModel);
					return result;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/updatenodename")
	public R<HashMap<String, Object>> updatenodename(String domain, String nodeid, String nodename) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		HashMap<String, Object> graphNodeList = new HashMap<String, Object>();
		try {
			if (!StringUtil.isBlank(domain)) {
				graphNodeList = KGGraphService.updatenodename(domain, nodeid, nodename);
				if (graphNodeList.size() > 0) {
					result.code = 200;
					result.setData(graphNodeList);
					return result;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}
	@ResponseBody
	@RequestMapping(value = "/updateCorrdOfNode")
	public R<String> updateCorrdOfNode(String domain, String uuid, Double fx, Double fy) {
		R<String> result = new R<String>();
		try {
			KGGraphService.updateCorrdOfNode(domain, uuid, fx, fy);
			result.code = 200;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}
	@ResponseBody
	@RequestMapping(value = "/createnode")
	public R<HashMap<String, Object>> createnode(QAEntityItem entity, HttpServletRequest request,
			HttpServletResponse response) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		HashMap<String, Object> graphNode = new HashMap<String, Object>();
		try {
			String domain = request.getParameter("domain");
			graphNode=KGGraphService.createnode(domain, entity);
			if (graphNode!=null&&graphNode.size() > 0) {
				result.code = 200;
				result.setData(graphNode);
				return result;
			}
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}

		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/batchcreatenode")
	public R<HashMap<String, Object>> batchcreatenode(String domain, String sourcename, String[] targetnames,
			String relation) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		HashMap<String, Object> rss = new HashMap<String, Object>();
		try {
			rss= KGGraphService.batchcreatenode(domain, sourcename, relation, targetnames);
			result.code = 200;
			result.setData(rss);
			return result;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}

		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/batchcreatechildnode")
	public R<HashMap<String, Object>> batchcreatechildnode(String domain, String sourceid, Integer entitytype,
			String[] targetnames, String relation) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		HashMap<String, Object> rss = new HashMap<String, Object>();
		try {
			rss= KGGraphService.batchcreatechildnode(domain, sourceid, entitytype, targetnames, relation);
			result.code = 200;
			result.setData(rss);
			return result;

		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}

		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/batchcreatesamenode")
	public R<List<HashMap<String, Object>>> batchcreatesamenode(String domain, Integer entitytype,
			String[] sourcenames) {
		R<List<HashMap<String, Object>>> result = new R<List<HashMap<String, Object>>>();
		List<HashMap<String, Object>> rss = new ArrayList<HashMap<String, Object>>();
		try {
			rss=KGGraphService.batchcreatesamenode(domain, entitytype, sourcenames);
			result.code = 200;
			result.setData(rss);
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}

		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/createlink")
	public R<HashMap<String, Object>> createlink(String domain, long sourceid, long targetid, String ship) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		try {
			HashMap<String, Object> cypherResult = KGGraphService.createlink(domain, sourceid, targetid, ship);
			result.code = 200;
			result.setData(cypherResult);
			return result;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}

		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/updatelink")
	public R<HashMap<String, Object>> updatelink(String domain, long shipid, String shipname) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		try {
			HashMap<String, Object> cypherResult = KGGraphService.updatelink(domain, shipid, shipname);
			result.code = 200;
			result.setData(cypherResult);
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/deletenode")
	public R<List<HashMap<String, Object>>> deletenode(String domain, long nodeid) {
		R<List<HashMap<String, Object>>> result = new R<List<HashMap<String, Object>>>();
		try {
			List<HashMap<String, Object>> rList = KGGraphService.deletenode(domain, nodeid);
			result.code = 200;
			result.setData(rList);
			return result;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/deletedomain")
	public R<List<HashMap<String, Object>>> deletedomain(Integer domainid, String domain) {
		R<List<HashMap<String, Object>>> result = new R<List<HashMap<String, Object>>>();
		try {
			kgservice.deleteDomain(domainid);
			KGGraphService.deleteKGdomain(domain);
			result.code = 200;
			return result;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/deletelink")
	public R<HashMap<String, Object>> deletelink(String domain, long shipid) {
		R<HashMap<String, Object>> result = new R<HashMap<String, Object>>();
		try {
			KGGraphService.deletelink(domain, shipid);
			result.code = 200;
			return result;
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/importgraph")
	public JSONObject importgraph(@RequestParam(value = "file", required = true) MultipartFile file,
								  HttpServletRequest request, HttpServletResponse response) throws Exception {
		JSONObject res = new JSONObject();
		if (file == null) {
			res.put("code", "500");
			res.put("msg", "请先选择有效的文件");
			return res;
		}
		// 领域不能为空
		String label = request.getParameter("domain");
		if (StringUtil.isBlank(label)) {
			res.put("code", "500");
			res.put("msg", "请先选择领域");
			return res;
		}
		List<Map<String, Object>> dataList = getFormatData(file);
		try {
			List<List<String>> list = new ArrayList<>();
			for (Map<String, Object> item : dataList) {
				List<String> lst = new ArrayList<>();
				lst.add(item.get("sourcenode").toString());
				lst.add(item.get("targetnode").toString());
				lst.add(item.get("relationship").toString());
				list.add(lst);
			}
			String savePath = config.getLocation();
			String filename = "tc" + System.currentTimeMillis() + ".csv";
			CSVUtil.createCsvFile(list, savePath,filename);
			String serverUrl=request.getServerName() + ":" + request.getServerPort() + request.getContextPath();
			String csvUrl = "http://"+serverUrl+ "/download/" + filename;
			//String csvUrl = "https://neo4j.com/docs/cypher-manual/3.5/csv/artists.csv";
			KGGraphService.batchInsertByCSV(label, csvUrl, 0);
			res.put("code", 200);
			res.put("message", "success!");
			return res;
		} catch (Exception e) {
			res.put("code", 500);
			res.put("message", "服务器错误!");
		}
		return res;
	}
	private List<Map<String, Object>> getFormatData(MultipartFile file) throws Exception {
		List<Map<String, Object>> mapList = new ArrayList<>();
		try {
			String fileName = file.getOriginalFilename();
			if (!fileName.endsWith(".csv")) {
				Workbook workbook = null;
				if (ExcelUtil.isExcel2007(fileName)) {
					workbook = new XSSFWorkbook(file.getInputStream());
				} else {
					workbook = new HSSFWorkbook(file.getInputStream());
				}
				// 有多少个sheet
				int sheets = workbook.getNumberOfSheets();
				for (int i = 0; i < sheets; i++) {
					Sheet sheet = workbook.getSheetAt(i);
					int rowSize = sheet.getPhysicalNumberOfRows();
					for (int j = 0; j < rowSize; j++) {
						Row row = sheet.getRow(j);
						int cellSize = row.getPhysicalNumberOfCells();
						if (cellSize != 3) continue; //只读取3列
						row.getCell(0).setCellType(Cell.CELL_TYPE_STRING);
						Cell cell0 = row.getCell(0);//节点1
						row.getCell(1).setCellType(Cell.CELL_TYPE_STRING);
						Cell cell1 = row.getCell(1);//节点2
						row.getCell(2).setCellType(Cell.CELL_TYPE_STRING);
						Cell cell2 = row.getCell(2);//关系
						if (null == cell0 || null == cell1 || null == cell2) {
							continue;
						}
						String sourceNode = cell0.getStringCellValue();
						String targetNode = cell1.getStringCellValue();
						String relationShip = cell2.getStringCellValue();
						if (StringUtil.isBlank(sourceNode) || StringUtils.isBlank(targetNode) || StringUtils.isBlank(relationShip))
							continue;
						Map<String, Object> map = new HashMap<String, Object>();
						map.put("sourcenode", sourceNode);
						map.put("targetnode", targetNode);
						map.put("relationship", relationShip);
						mapList.add(map);
					}
				}
			} else if (fileName.endsWith(".csv")) {
				List<List<String>> list = CSVUtil.readCsvFile(file);
				for (int i = 0; i < list.size(); i++) {
					List<String> lst = list.get(i);
					if (lst.size() != 3) continue;
					String sourceNode = lst.get(0);
					String targetNode = lst.get(1);
					String relationShip = lst.get(2);
					if (StringUtil.isBlank(sourceNode) || StringUtils.isBlank(targetNode) || StringUtils.isBlank(relationShip))
						continue;
					Map<String, Object> map = new HashMap<String, Object>();
					map.put("sourcenode", sourceNode);
					map.put("targetnode", targetNode);
					map.put("relationship", relationShip);
					mapList.add(map);
				}
			}
		} catch (Exception ex) {
			throw new Exception(ex);
		}
		return mapList;
	}
	@ResponseBody
	@RequestMapping(value = "/exportgraph")
	public JSONObject exportgraph(HttpServletRequest request, HttpServletResponse response) throws Exception {
		JSONObject res = new JSONObject();
		String label = request.getParameter("domain");
		String filePath = config.getLocation();
		String fileName = UUID.randomUUID() + ".csv";
		String fileUrl = filePath + File.separator + fileName;
		String cypher = String.format(
				"MATCH (n:%s) -[r]->(m:%s) return n.name as source,m.name as target,r.name as relation", label, label);
		List<HashMap<String, Object>> list = neo4jUtil.GetGraphItem(cypher);
		File file = new File(fileUrl);
		try {
			if (!file.exists()) {
				file.createNewFile();
				System.out.println("文件不存在，新建成功！");
			} else {
				System.out.println("文件存在！");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		CsvWriter csvWriter = new CsvWriter(fileUrl, ',', Charset.forName("UTF-8"));
		String[] header = { "source", "target", "relation" };
		csvWriter.writeRecord(header);
		for (HashMap<String, Object> hashMap : list) {
			int colSize = hashMap.size();
			String[] cntArr = new String[colSize];
			cntArr[0] = hashMap.get("source").toString().replace("\"", "");
			cntArr[1] = hashMap.get("target").toString().replace("\"", "");
			cntArr[2] = hashMap.get("relation").toString().replace("\"", "");
			try {
				csvWriter.writeRecord(cntArr);
			} catch (IOException e) {
				log.error("CSVUtil->createFile: 文件输出异常" + e.getMessage());
			}
		}
		csvWriter.close();
		String serverUrl=request.getServerName() + ":" + request.getServerPort() + request.getContextPath();
		String csvUrl = serverUrl + "/kg/download/" + fileName;
		res.put("code", 200);
		res.put("csvurl", csvUrl);
		res.put("message", "success!");
		return res;

	}

	// 文件下载相关代码
	@GetMapping(value = "/download/{filename}")
	public String download(@PathVariable("filename") String filename, HttpServletRequest request,
						   HttpServletResponse response) {
		String filePath = config.getLocation();
		String fileUrl = filePath + filename;
		if (fileUrl != null) {
			File file = new File(fileUrl);
			if (file.exists()) {
				//response.setContentType("application/force-download");// 设置强制下载不打开
				response.addHeader("Content-Disposition", "attachment;fileName=" + filename+".csv");// 设置文件名
				byte[] buffer = new byte[1024];
				FileInputStream fis = null;
				BufferedInputStream bis = null;
				try {
					fis = new FileInputStream(file);
					bis = new BufferedInputStream(fis);
					OutputStream os = response.getOutputStream();
					int i = bis.read(buffer);
					while (i != -1) {
						os.write(buffer, 0, i);
						i = bis.read(buffer);
					}
					System.out.println("success");
				} catch (Exception e) {
					e.printStackTrace();
				} finally {
					if (bis != null) {
						try {
							bis.close();
						} catch (IOException e) {
							e.printStackTrace();
						}
					}
					if (fis != null) {
						try {
							fis.close();
						} catch (IOException e) {
							e.printStackTrace();
						}
					}
				}
			}
		}
		return null;
	}

	@ResponseBody
	@RequestMapping(value = "/getnodeimage")
	public R<List<Map<String, Object>>> getNodeImagelist(int domainid, int nodeid) {
		R<List<Map<String, Object>>> result = new R<List<Map<String, Object>>>();
		try {
			List<Map<String, Object>> images = kgservice.getNodeImageList(domainid, nodeid);
			result.code = 200;
			result.setData(images);
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/getnodecontent")
	public R<Map<String, Object>> getNodeContent(int domainid, int nodeid) {
		R<Map<String, Object>> result = new R<Map<String, Object>>();
		try {
			List<Map<String, Object>> contents = kgservice.getNodeContent(domainid, nodeid);
			if (contents != null && contents.size() > 0) {
				result.code = 200;
				result.setData(contents.get(0));
			}
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}
	@CrossOrigin
	@ResponseBody
	@RequestMapping(value = "/getnodedetail")
	public R<Map<String, Object>> getNodeDetail(int domainid, int nodeid) {
		R<Map<String, Object>> result = new R<Map<String, Object>>();
		try {
			Map<String, Object> res = new HashMap<String, Object>();
			res.put("content", "");
			res.put("imagelist", new String[] {});
			List<Map<String, Object>> contents = kgservice.getNodeContent(domainid, nodeid);
			if (contents != null && contents.size() > 0) {
				res.replace("content", contents.get(0).get("Content"));
			}
			List<Map<String, Object>> images = kgservice.getNodeImageList(domainid, nodeid);
			if (images != null && images.size() > 0) {
				res.replace("imagelist", images);
			}
			result.code = 200;
			result.setData(res);
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/savenodeimage")
	public R<String> saveNodeImage(@RequestBody Map<String, Object> params) {
		R<String> result = new R<String>();
		try {
			String username = "tc";
			int domainid = (int) params.get("domainid");
			String nodeid = params.get("nodeid").toString();
			String imagelist = params.get("imagelist").toString();
			List<Map<String, Object>> domainList = kgservice.getDomainById(domainid);
			if (domainList != null && domainList.size() > 0) {
				String domainName = domainList.get(0).get("name").toString();
				kgservice.deleteNodeImage(domainid, Integer.parseInt(nodeid));
				List<Map> imageItems = JSON.parseArray(imagelist, Map.class);
				List<Map<String, Object>> submitItemList = new ArrayList<Map<String, Object>>();
				if (!imageItems.isEmpty()) {
					for (Map<String, Object> item : imageItems) {
						String file = item.get("fileurl").toString();
						int sourcetype = 0;
						Map<String, Object> sb = new HashMap<String, Object>();
						sb.put("file", file);
						sb.put("imagetype", sourcetype);
						sb.put("domainid", domainid);
						sb.put("nodeid", nodeid);
						sb.put("status", 1);
						sb.put("createuser", username);
						sb.put("createtime", DateUtil.getDateNow());
						submitItemList.add(sb);
					}
				}
				if (submitItemList != null && submitItemList.size() > 0) {
					kgservice.saveNodeImage(submitItemList);
					// 更新到图数据库,表明该节点有附件,加个标识,0=没有,1=有
					KGGraphService.updateNodeFileStatus(domainName, Long.parseLong(nodeid), 1);
					result.code = 200;
					result.setMsg("操作成功");
				} else {
					KGGraphService.updateNodeFileStatus(domainName, Long.parseLong(nodeid), 0);
					result.code = 200;
					result.setMsg("操作成功");
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

	@ResponseBody
	@RequestMapping(value = "/savenodecontent")
	public R<String> savenodecontent(@RequestBody Map<String, Object> params) {
		R<String> result = new R<String>();
		try {
			String username = "tc";
			int domainid = (int) params.get("domainid");
			String nodeid = params.get("nodeid").toString();
			String content = params.get("content").toString();
			List<Map<String, Object>> domainList = kgservice.getDomainById(domainid);
			if (domainList != null && domainList.size() > 0) {
				String domainName = domainList.get(0).get("name").toString();
				// 检查是否存在
				List<Map<String, Object>> items = kgservice.getNodeContent(domainid, Integer.parseInt(nodeid));
				if (items != null && items.size() > 0) {
					Map<String, Object> olditem = items.get(0);
					Map<String, Object> item = new HashMap<String, Object>();
					item.put("domainid", olditem.get("DomainId"));
					item.put("nodeid", olditem.get("NodeId"));
					item.put("content", content);
					item.put("modifyuser", username);
					item.put("modifytime", DateUtil.getDateNow());
					kgservice.updateNodeContent(item);
					result.code = 200;
					result.setMsg("更新成功");
				} else {
					Map<String, Object> sb = new HashMap<String, Object>();
					sb.put("content", content);
					sb.put("domainid", domainid);
					sb.put("nodeid", nodeid);
					sb.put("status", 1);
					sb.put("createuser", username);
					sb.put("createtime", DateUtil.getDateNow());
					if (sb != null && sb.size() > 0) {
						kgservice.saveNodeContent(sb);
						result.code = 200;
						result.setMsg("保存成功");
					}
				}
				// 更新到图数据库,表明该节点有附件,加个标识,0=没有,1=有
				KGGraphService.updateNodeFileStatus(domainName, Long.parseLong(nodeid), 1);
			}

		} catch (Exception e) {
			e.printStackTrace();
			result.code = 500;
			result.setMsg("服务器错误");
		}
		return result;
	}

}
