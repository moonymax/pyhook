package com.moonymax.pyhook;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.lang.ProcessBuilder.Redirect;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.bukkit.Bukkit;
import org.bukkit.command.CommandMap;
import org.bukkit.command.PluginCommand;
import org.bukkit.command.defaults.BukkitCommand;
import org.bukkit.event.Event;
import org.bukkit.event.EventException;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.HandlerList;
import org.bukkit.event.Listener;
import org.bukkit.plugin.EventExecutor;
import org.bukkit.plugin.RegisteredListener;
import org.bukkit.plugin.java.JavaPlugin;

import io.github.classgraph.ClassGraph;
import io.github.classgraph.ClassInfo;
import io.github.classgraph.ClassInfoList;
import py4j.ClientServer;
import py4j.GatewayServer;
import py4j.reflection.ReflectionUtil;
import py4j.reflection.RootClassLoadingStrategy;

/*
 * test java plugin
 */

public class Plugin extends JavaPlugin implements Listener, EventExecutor {
  private static final Logger LOGGER = Logger.getLogger("pyhook");

  EventListener listener;
  Process process;
  ClientServer clientServer;

  List<BukkitCommand> commands = new ArrayList<>();

  public BukkitCommand getCommandByName(String alias) {
    for (BukkitCommand command : commands) {
      if (command.getAliases().contains(alias)) {
        return command;
      }
    }
    return null;
  }

  public void registerCommand(String name, String usage, String description, String permission, List<String> aliases) {
    BukkitCommand command = getCommandByName(name);
    if (command != null) {
      command.unregister(getCommandMap());
    }

    if (permission == null)
      permission = name + ".command";
    if (usage == null)
      usage = "";
    if (description == null)
      description = "";
    if (aliases == null)
      aliases = new ArrayList<String>();

    registerDynamicCommand(command, name, usage, description, permission, aliases);
  }

  private void registerDynamicCommand(BukkitCommand command, String name, String usage, String description,
      String permission,
      List<String> aliases) {
    aliases.add(0, name);
    BukkitCommand newCommand = new DynamicCommand(this, permission, name, description, usage, aliases);
    if (command == null) {
      commands.add(newCommand);
    } else {
      command = newCommand;
    }
  }

  public CommandMap getCommandMap() {
    CommandMap commandMap = null;

    try {
      Field f = Bukkit.getPluginManager().getClass().getDeclaredField("commandMap");
      f.setAccessible(true);

      commandMap = (CommandMap) f.get(Bukkit.getPluginManager());
    } catch (NoSuchFieldException | IllegalAccessException | IllegalArgumentException | SecurityException e) {
      e.printStackTrace();
    }

    return commandMap;
  }

  @Override
  public void execute(Listener listener, Event event) throws EventException {
    // listener is null when python isnt running yet
    if (this.listener != null) {
      Object returnValue = this.listener.onEvent(this, "SpigotEvent", event);
      // event = (Event) returnValue;
    }
  }

  @Override
  public void onEnable() {

    // get all the non abstract Event class names
    ClassInfoList events = new ClassGraph()
        .enableClassInfo()
        .scan() // you should use try-catch-resources instead
        .getClassInfo(Event.class.getName())
        .getSubclasses()
        .filter(info -> !info.isAbstract());

    try {
      for (ClassInfo event : events) {
        Class<? extends Event> eventClass = (Class<? extends Event>) Class.forName(event.getName());

        // this is more readable
        for (Method method : eventClass.getDeclaredMethods()) {
          if (method.getParameterCount() == 0 && method.getName().equals("getHandlers")) {
            getServer().getPluginManager().registerEvent(eventClass, this,
                EventPriority.NORMAL, this, this);
          }
        }

        /*
         * if (Arrays.stream(eventClass.getDeclaredMethods())
         * .anyMatch(method -> method.getParameterCount() == 0 &&
         * method.getName().equals("getHandlers"))) {
         * getServer().getPluginManager().registerEvent(eventClass, this,
         * EventPriority.NORMAL, this, this);
         * }
         */
      }
    } catch (ClassNotFoundException e) {
      throw new AssertionError("Scanned class wasn't found", e);
    }

    String[] eventNames = events.stream()
        .map(info -> info.getName().substring(info.getName().lastIndexOf('.') + 1))
        .toArray(String[]::new);

    // LOGGER.info("List of events:\n" + String.join("\n", eventNames));

    LOGGER.info("Events found: " + events.size());
    LOGGER.info("HandlerList size: " + HandlerList.getHandlerLists().size());

    RootClassLoadingStrategy rmmClassLoader = new RootClassLoadingStrategy();
    ReflectionUtil.setClassLoadingStrategy(rmmClassLoader);

    ProcessBuilder processBuilder = new ProcessBuilder().command("./venv/bin/python", "pyhook.py");
    processBuilder.redirectOutput(Redirect.INHERIT);
    processBuilder.redirectError(Redirect.INHERIT);

    try {
      process = processBuilder.start();
    } catch (IOException e) {
      LOGGER.log(Level.SEVERE, "Failed to start python process!\n" + e.getMessage());
    }
    try {
      Thread.sleep(2000);
    } catch (Exception e) {
      e.printStackTrace();
    }
    // start connection from here
    clientServer = new ClientServer(null);

    listener = (EventListener) clientServer.getPythonServerEntryPoint(new Class[] { EventListener.class });
    listener.onEvent(this, "EnableEvent", null);

    LOGGER.info("pyhook enabled");
  }

  @Override
  public void onDisable() {
    if (this.listener != null) {
      this.listener.onEvent(this, "stop", null);
    }
    clientServer.shutdown();
    try {
      process.waitFor(3, TimeUnit.SECONDS);
    } catch (Exception e) {
      LOGGER.log(Level.SEVERE,
          "Java main process was interupted while waiting for python process to finish\n"
              + e.getMessage());
      e.printStackTrace();
      process.destroy();
    }

    LOGGER.info("pyhook disabled");
  }

}
