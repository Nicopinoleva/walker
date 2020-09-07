package com.zolbit;

import java.util.HashMap;
import java.util.Map;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.support.ui.Select;
import org.python.util.PythonInterpreter;
import org.sikuli.script.ImagePath;
import org.sikuli.script.Key;
import org.sikuli.script.Button;
import org.sikuli.script.Screen;
import org.sikuli.script.Mouse;
import org.sikuli.script.Region;
import org.sikuli.script.App;
import org.sikuli.script.FindFailed;
import org.sikuli.script.Match;
import org.sikuli.basics.Debug;
import org.sikuli.basics.Settings;

import java.io.*;
import java.nio.file.*;
import java.net.*;

import org.apache.commons.cli.*;

public class Walker {
	//Variables estáticas. Estas son solo por clase, debido a que no cambian.
	public static final String DOWN = Key.DOWN;
	public static final String UP = Key.UP;
	public static final String RIGHT = Key.RIGHT;
	public static final String LEFT = Key.LEFT;
	public static final String TAB = Key.TAB;
	public static final String ENTER = Key.ENTER;
	public static final String ESC = Key.ESC;
	public static final String DELETE = Key.DELETE;
	public static final String PAGE_DOWN = Key.PAGE_DOWN;
	public static final String PAGE_UP = Key.PAGE_UP;
	public static final String CTRL = Key.CTRL;
	public static final String SHIFT = Key.SHIFT;
	public static final String ALT = Key.ALT;
	public static final String SPACE = Key.SPACE;
	public static final int MOUSE_LEFT = Button.LEFT;
	public static final int MOUSE_MIDDLE = Button.MIDDLE;
	public static final int MOUSE_RIGHT = Button.RIGHT;
	//Variables privadas dinámicas.
	private String TCP_ENGINE;
	private Socket client_socket;
	private int c_socket;
	//Variables dinámicas. Estas es mejor mantenerlas por instancia en caso de querer instanciar más de un walker.
	public String PATHFILE;
	public String DEFAULT_DOWNLOAD_DIRECTORY;
	public String WEBDRIVER_DIRECTORY;
	public String IMAGEPATH;
	public String SCREENSHOT_DIRECTORY;
	public ChromeDriver main_driver_c;
	public FirefoxDriver main_driver_f;
	public Boolean USE_FIREFOX;
	public Boolean ENABLE_FLASH;
	public Screen screen;
	//Métodos estáticos
	//Privados: Solo se pueden usar dentro de walker.
	private static String append_slash(String s) {
		if (s.charAt(s.length() - 1) != '/') {
			return s + "/";
		}
		return s;
	}
	public static void log(String code, String s) throws Exception {
		/*String MSG_UNKNOWN_CODE = "Código de log no encontrado.";
		Map<String, String> codes = new HashMap<>();
		codes.put("ERROR", "ERROR");
		codes.put("CONF", "CONF ");
		codes.put("DEBUG", "DEBUG");
		codes.put("INFO", "INFO ");
		codes.put("WARNING", "WARNING");
		if (!codes.containsKey(code)) {
			throw new Exception(MSG_UNKNOWN_CODE);
		}
		System.out.println("["+codes.get(code)+"]" + s);*/
		System.out.println(s);
	}
	//Métodos dinámicos
	//Públicos: Se pueden usar dentro y fuera de walker.
	//Constructor
	public Walker() {
		PATHFILE = "/";
		DEFAULT_DOWNLOAD_DIRECTORY = "Downloads/";
		WEBDRIVER_DIRECTORY = "/";
		IMAGEPATH = "Images/";
		SCREENSHOT_DIRECTORY = "Screenshots/";
		TCP_ENGINE = "C";//Realiza la comunicaci�n con el agente en C
		ENABLE_FLASH = false;//Evita que chrome pida persimo para ejecutar p�ginas flash
		USE_FIREFOX = false;//Si se cambia a True desde caminos usando python_wrapper ejecuta chrome
	}
	//Métodos de configuración
	public void set_min_similarity(double value) throws Exception{
		String MESSAGE_MIN_SIMILARITY = "MIN SIMILARITY set.";
		Settings.MinSimilarity = value;
		log("CONF", MESSAGE_MIN_SIMILARITY);
	}
	public void set_imagepath(String IMAGEPATH) throws Exception{
		String MESSAGE_IMAGEPATH_SET = "IMAGEPATH set.";
		ImagePath.setBundlePath(append_slash(IMAGEPATH));
		log("CONF", MESSAGE_IMAGEPATH_SET);
	}
	public void set_download_directory(String DOWNLOAD_PATH) throws Exception{
		String MESSAGE_DOWNLOAD_SET = "DOWNLOAD_PATH set.";
		DEFAULT_DOWNLOAD_DIRECTORY = append_slash(DOWNLOAD_PATH);
		log("CONF", MESSAGE_DOWNLOAD_SET);
	}
	public void set_screenshot_directory(String SCREENSHOT_PATH) throws Exception{
		String MESSAGE_SCREENSHOT_SET = "SCREENSHOT_PATH set.";
		SCREENSHOT_DIRECTORY = append_slash(SCREENSHOT_PATH);
		log("CONF", MESSAGE_SCREENSHOT_SET);
	}
	public void set_webdriver_directory(String directory) throws Exception {
		String MESSAGE_WEBDRIVER_SET = "WEBDRIVER set.";
		System.setProperty("webdriver.chrome.driver", append_slash(directory));
		log("CONF", MESSAGE_WEBDRIVER_SET);
	}
	public void enable_flash(Boolean enabled) throws Exception {
		String MESSAGE_FLASH = "FLASH set.";
		ENABLE_FLASH = enabled;
		log("CONF", MESSAGE_FLASH);
	}
	public void use_firefox(Boolean enabled) throws Exception {
		String MESSAGE_EXPLORER = "Firefox set.";
		USE_FIREFOX = enabled;
		log("CONF", MESSAGE_EXPLORER);
	}
	//Métodos de funcionalidad
	private By getByIdentifier(String identifier) {
        String[] identifiers = identifier.split("=");

        return identifiers[0].equals("id") ? By.id(identifiers[1]) :
                By.className(identifiers[1]);
    }
	private WebElement expandRootElement(WebElement element) {
        return (WebElement) main_driver_c.executeScript("return arguments[0].shadowRoot",element);
    }
	public void launch_explorer(String url) throws Exception {
		if (!USE_FIREFOX) {
			ChromeOptions options = new ChromeOptions();
			Map<String, Object> prefs = new HashMap<String, Object>();
			log("DEBUG", "DEFAULT_DOWNLOAD_DIRECTORY = " + DEFAULT_DOWNLOAD_DIRECTORY);
			prefs.put("download.default_directory", DEFAULT_DOWNLOAD_DIRECTORY);
			prefs.put("download.prompt_for_download", true);
			options.setExperimentalOption("prefs", prefs);
			if (ENABLE_FLASH) {//SOLO PARA CHROME
				options.addArguments("--no-sandbox","--disable-dev-shm-usage","RunAllFlashInAllowMode","--start-maximized"
						,"disable-features=EnableEphemeralFlashPermission",
						"user-data-dir=/home/seluser/.config/google-chrome/Profile 2","--enable-popup-blocking");
				this.main_driver_c = new ChromeDriver(options);
				this.main_driver_c.get("chrome://settings/content/siteDetails?site=" + url);
				WebElement root1 = main_driver_c.findElement(By.tagName("settings-ui"));
				WebElement shadowRoot1 = expandRootElement(root1);
				WebElement root2 = shadowRoot1.findElement(getByIdentifier("id=container"));
				WebElement main = root2.findElement(getByIdentifier("id=main"));
				WebElement shadowRoot3 = expandRootElement(main);
				WebElement shadowRoot4 = shadowRoot3.findElement(getByIdentifier("class=showing-subpage"));
				WebElement shadowRoot5 = expandRootElement(shadowRoot4);
				WebElement shadowRoot6 = shadowRoot5.findElement(getByIdentifier("id=advancedPage"));
				WebElement shadowRoot7 = shadowRoot6.findElement(By.tagName("settings-privacy-page"));
				WebElement shadowRoot8 = expandRootElement(shadowRoot7);
				WebElement shadowRoot9 = shadowRoot8.findElement(getByIdentifier("id=pages"));
				WebElement shadowRoot10 = shadowRoot9.findElement(By.tagName("settings-subpage"));
				WebElement shadowRoot11 = shadowRoot10.findElement(By.tagName("site-details"));
				WebElement shadowRoot12 = expandRootElement(shadowRoot11);
				WebElement shadowRoot13 = shadowRoot12.findElement(By.id("plugins"));
				WebElement shadowRoot14 = expandRootElement(shadowRoot13);
				new Select(shadowRoot14.findElement(By.id("permission"))).selectByValue("allow");
			}
			else {
				options.addArguments("--no-sandbox","--enable-popup-blocking","--start-maximized","--disable-dev-shm-usage");
				this.main_driver_c = new ChromeDriver(options);
			}
			this.main_driver_c.get(url);
		}
		else {
			FirefoxOptions options = new FirefoxOptions();
			FirefoxProfile profile = new FirefoxProfile();
			profile.setPreference("browser.download.useDownloadDir", false);
			profile.setPreference("browser.helperApps.neverAsk.saveToDisk", "application/unzip");
			options.setProfile(profile);
			main_driver_f = new FirefoxDriver(options);
			this.main_driver_f.get(url);
		}
	}
	public void close_explorer() throws Exception {
		if (!USE_FIREFOX) {
			this.main_driver_c.quit();
		}
		else {
			this.main_driver_f.quit();
		}
	}
	public double image_click(String img, int timeout) throws Exception {
		Match m = screen.exists(img, timeout);
		double score = 0.0d;
		if (m != null)
			score = m.getScore();
		screen.click(img);
		return score;
	}
	public void click() throws Exception {
		screen.click(Mouse.at());
	}
	public int mouse_get_x() throws Exception {
		return Mouse.at().x;
	}
	public int mouse_get_y() throws Exception {
		return Mouse.at().y;
	}
	public void mouse_move(int x, int y) throws Exception {
		screen.mouseMove(x, y);
	}
	public double double_click(String img, int timeout) throws Exception {
		Match m = screen.exists(img, timeout);
		double score = 0.0d;
		if (m != null)
			score = m.getScore();
		screen.doubleClick(img);
		return score;
	}
	public double right_click(String img, int timeout) throws Exception {
		Match m = screen.exists(img, timeout);
		double score = 0.0d;
		if (m != null)
			score = m.getScore();
		screen.rightClick(img);
		return score;
	}
	public void type(String text) throws Exception {
		screen.paste(text);
	}
	public void press(String key) throws Exception {
		screen.type(key);
	}
	public void key_down(String key) throws Exception {
		screen.keyDown(key);
	}
	public void key_up(String key) throws Exception {
		screen.keyUp(key);
	}
	public double hover(String img, int timeout) throws Exception {
		Match m = screen.exists(img, timeout);
		double score = 0.0d;
		if (m != null)
			score = m.getScore();
		screen.hover(img);
		return score;
	}
	public void mouse_down(int button) throws Exception {
		screen.mouseDown(button);
	}
	public void mouse_up(int button) throws Exception {
		screen.mouseUp(button);
	}
	public String get_clipboard() throws Exception {
		return App.getClipboard();
	}
	public void wait(int millis) throws Exception {
		Thread.sleep(millis);
	}
	public void image_wait(String img, int timeout) throws Exception {
		if (screen.exists(img, timeout) != null) {
			return;
		}
		throw new FindFailed("La imagen no aparecio nunca. (image_wait)");
	}
	public void image_gone_wait(String img, int timeout) throws Exception {
		float retry_time = 0.5f;
		float time_acc = 0;
		while (screen.exists(img, 1) != null) {
			Thread.sleep((int) retry_time * 1000);
			time_acc += retry_time;
			if (time_acc >= timeout) {
				tcp_send("FAILED");
				throw new ImageNotGone("La imagen no desaparecio nunca. (image_gone_wait)");
			}
		}
	}
	public Boolean image_appeared(String img, int timeout) throws Exception {
		return (screen.exists(img, timeout) != null);
	}
	public String image_wait_multiple(String []imgs, int timeout) throws Exception {
		/*
		 * Recibe una lista de imagenes, y retorna el string de la imagen que encontró.
		 * Si no la encuentra en el timeout dado, retorna una excepción.
		 */
		double retry_time = 0.5f;
		double time_acc = 0;
		while (true) {
			for (int i = 0; i != imgs.length; i++) {
				if (screen.exists(imgs[i], retry_time) != null) {
					return imgs[i];
				}
				time_acc += retry_time;
				if (time_acc >= timeout) {
					return "";
				}
			}
		}
	}
	public void init_screen() throws Exception {
		this.screen = new Screen();
	}
	//Métodos TCP
	public void tcp_connect(String host) throws Exception{
		if (!host.contains(":")) {
			throw new Exception("Direccion host mal formada: " + host);
		}
		String[] output = host.split(":");
		String ip = output[0];
		int port = Integer.parseInt(output[1]);
		if (TCP_ENGINE == "JAVA") {
			client_socket = new Socket(ip, port);
		} else if (TCP_ENGINE == "C") {
			c_socket = TCPClient.conecta(ip, port);
		}
	}
	public void tcp_send(String message) throws Exception {
		if (TCP_ENGINE == "JAVA") {
			OutputStream os = client_socket.getOutputStream();
			byte[] b = message.getBytes();
			os.write(b, 0, b.length);
		} else if (TCP_ENGINE == "C") {
			TCPClient.enviar_mensaje(message, c_socket);
		}
	}
	public void tcp_close() throws Exception {
		if (TCP_ENGINE == "JAVA") {
			client_socket.close();
		} else if (TCP_ENGINE == "C") {
			
		}
	}
	public void screenshot_save(String filename) throws Exception {
		String fullpath = SCREENSHOT_DIRECTORY + filename + ".png";
		int error_code = Screenshot.save(fullpath);
		if (error_code == 0) {
			log("INFO", "Captura guardada: " + fullpath);
		} else {
			log("ERROR", "Captura NO guardada: " + fullpath);
			throw new Exception("No se pudo guardar la captura de pantalla.");
		}
	}
	public void screenshot_save_crop(String filename, int x1, int y1, int x2, int y2) throws Exception {
		String fullpath = SCREENSHOT_DIRECTORY + filename + ".png";
		int error_code = Screenshot.save_crop(fullpath, x1, y1, x2, y2);
		if (error_code == 0) {
			log("INFO", "Captura guardada: " + fullpath);
		} else {
			log("ERROR", "Captura NO guardada: " + fullpath);
			throw new Exception("No se pudo guardar la captura de pantalla.");
		}
	}
	public static void zip_folder(String folder_directory, String zip_filename) throws Exception {
		ZipFolder.zipper(folder_directory, zip_filename);
	}
	public static void print(String s) throws Exception {
		System.out.println("[Walker]" + s);
	}
	public String get_url() throws Exception {
		String url;
		if (!USE_FIREFOX) {
			url = this.main_driver_c.getCurrentUrl();
		}
		else {
			url = this.main_driver_f.getCurrentUrl();
		}
		return url;
	}
	// public static void main_with_options(String[] args) throws Exception {
	// 	Options options = new Options();

 //        Option input = new Option("i", "input", true, "ruta del archivo de input");
 //        input.setRequired(true);
 //        options.addOption(input);
        
 //        Option port = new Option("p", "port", true, "numero de puerto");
 //        port.setRequired(true);
 //        options.addOption(port);
        
 //        Option log_id = new Option("l", "logid", true, "log id");
 //        log_id.setRequired(true);
 //        options.addOption(log_id);
        
 //        Option retries = new Option("r", "retries", true, "numero de intentos");
 //        options.addOption(retries);
        
 //        Option trace = new Option("t", "trace_every", true, "cada cuantos archivos se debe reportar");
 //        options.addOption(trace);

 //        CommandLineParser parser = new GnuParser();
 //        HelpFormatter formatter = new HelpFormatter();
 //        CommandLine cmd = null;

 //        try {
 //            cmd = parser.parse(options, args);
 //        } catch (ParseException e) {
 //            System.out.println(e.getMessage());
 //            formatter.printHelp("utility-name", options);
 //            System.exit(1);
 //        }
 //        String wrapper_filename = "python_wrapper.py";
	// 	String filename = cmd.getOptionValue("input");
	// 	String option_logid = cmd.getOptionValue("logid");
	// 	String option_port = cmd.getOptionValue("port");
	// 	int option_retries = 1;
	// 	int option_trace_every = 100;
	// 	if (cmd.getOptionValue("retries") != null) {
	// 		option_retries = Integer.parseInt(cmd.getOptionValue("retries"));
	// 	}
	// 	if (cmd.getOptionValue("trace_every") != null) {
	// 		option_trace_every = Integer.parseInt(cmd.getOptionValue("trace_every"));
	// 	}
	// 	String[] option_args = cmd.getArgs();
	// 	String MESSAGE_EXECUTING = "Ejecutando " + filename;
	// 	//String MESSAGE_ENDED = filename + " ha terminado correctamente.";
	// 	PythonInterpreter pyInterp = new PythonInterpreter();
	// 	try {
	// 		pyInterp.set("OPTION_LOG_ID", option_logid);
	// 		pyInterp.set("OPTION_PORT", option_port);
	// 		pyInterp.set("OPTION_TRACE_EVERY", option_trace_every);
	// 		pyInterp.set("OPTION_FILENAME", filename);
	// 		pyInterp.set("OPTION_RETRIES", option_retries);
	// 		pyInterp.set("OPTION_ARGS", option_args);
	// 		log("INFO", MESSAGE_EXECUTING);
	// 		pyInterp.execfile(wrapper_filename);
	//     }
	// 	catch (Exception e) {
	// 		log("ERROR", "Error en entorno Jython. Detalle:\n" + e);
	// 	}
	// 	pyInterp.close();
	// }
	public static String get_jar_absolute_path() throws Exception {
		return Paths.get(Walker.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent().toString();
	}
	//Main
	public void run(String[] args) throws Exception {
		String abspath = append_slash(get_jar_absolute_path());
		//abspath = "";
		log("DEBUG", "Absolute path: " + abspath);
        String wrapper_filename = abspath + "python_wrapper.py";
        String filename = args[0];
		String MESSAGE_EXECUTING = "Ejecutando " + filename;
		PythonInterpreter pyInterp = new PythonInterpreter();
		try {
			pyInterp.set("OPTION_ARGS", args);
			pyInterp.set("ABSOLUTE_PATH", abspath);
			log("INFO", MESSAGE_EXECUTING);
			pyInterp.execfile(wrapper_filename);
	    }
		catch (Exception e) {
			log("ERROR", "Error en entorno Jython. Detalle:\n" + e);
		}
		pyInterp.close();
	}
	public void captcha_sb() throws Exception {
		Screenshot.save_crop("/home/seluser/Screenshots/captcha.png", 550, 456, 42, 45);
		Thread.sleep(3000);
		Region r = new Region(550,456,42,45);
		for(int i=0;i<5;i++) {
			if(r.exists("/home/seluser/Screenshots/captcha.png")!=null) {
				System.out.println("Es igual");
				int new_x = r.getX() + 50;
				r.setX(new_x);
			}
			else {
				if(i==1) {
					System.out.println("Est� entre 1ra y 2da, chequeando...");
					int new_x = r.getX() + 50;
					r.setX(new_x);
					if(r.exists("/home/seluser/Screenshots/captcha.png")==null) {
						System.out.println("Clickeando 1ra casilla");
						new_x = r.getX() - 100;
						System.out.println(new_x);
						r.setX(new_x);
						r.click();
					}
					else {
						Debug.info("Clickeando 2da casilla");
						Region r2 = new Region(600,456,42,45);
						r2.click();
					}
					break;
				}
				else {
					System.out.println("no es igual");
					r.click();
					break;	
				}
			}
		}
	}
	public void recaptchaGoogle(String CaptchaSolution, String CaptchaPath) {
		System.out.print("Ejecutando script recaptcha...");
		if (!USE_FIREFOX) {
			this.main_driver_c.executeScript("document.getElementById('g-recaptcha-response').style.display = 'block';");
			this.main_driver_c.findElementByXPath(CaptchaPath).sendKeys(CaptchaSolution);
		}
		else {
			this.main_driver_f.executeScript("document.getElementById('g-recaptcha-response').style.display = 'block';");
			this.main_driver_f.findElementByXPath(CaptchaPath).sendKeys(CaptchaSolution);
		}
		System.out.print("Script recaptcha ejecutado");
	}
	public static void main(String[] args) throws Exception {
		Walker w = new Walker();
		w.run(args);
	}
}
