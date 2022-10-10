package com.moonymax.pyhook;

import java.lang.reflect.Field;
import java.util.List;

import org.bukkit.Bukkit;
import org.bukkit.command.CommandMap;
import org.bukkit.command.CommandSender;
import org.bukkit.command.defaults.BukkitCommand;
import org.bukkit.entity.Player;

public class DynamicCommand extends BukkitCommand {
    Plugin plugin;

    public DynamicCommand(Plugin plugin, String permission, String name, String description, String usage,
            List<String> aliases) {
        super(name, description, usage, aliases);
        this.plugin = plugin;
        this.setName(name);
        this.setDescription(description);
        this.setUsage(usage);
        this.setAliases(aliases);
        this.setPermission(permission);
        try {
            Field f;
            f = Bukkit.getServer().getClass().getDeclaredField("commandMap");
            f.setAccessible(true);
            CommandMap commandMap = (CommandMap) f.get(Bukkit.getServer());
            commandMap.register(name, this);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean execute(CommandSender sender, String name, String[] args) {
        if (plugin.listener != null) {
            Object returnValue = plugin.listener.onEvent(plugin, "CommandEvent", new CommandObject(sender, name, args));
        }
        return true;

    }

}

class CommandObject {
    public CommandSender sender;
    public String name;
    public String[] args;

    CommandObject(CommandSender sender, String name, String[] args) {
        this.sender = sender;
        this.name = name;
        this.args = args;

    }

    public String getEventName() {
        return "onCommand";
    }

    public CommandSender getSender() {
        return this.sender;
    }

    public String getName() {
        return this.name;
    }

    public String[] getArgs() {
        return this.args;
    }
}