# Pyhook

Because noone should ever have to use java

Spigot plugins in python with Py4J

### Events

Event listeners can be created just by defining a function. A list of events can be found in the [example plugin](https://github.com/moonymax/pyhook/blob/master/installer/pyplugins/sampleplugin.py)

	def WeatherChangeEvent(**args):
	    event = args['event']
	    event.setCancelled(True)
	    print('weather change event was cancelled')
	
	
	def ThunderChangeEvent(**args):
	    event = args['event']
	    event.setCancelled(True)
	    print('thunder change event was cancelled')

	def onEnable(**args):  # is called when the connection to java was established
	    g = args['gateway']
	    world = g.jvm.org.bukkit.Bukkit.getServer().getWorld("world")
	    world.setStorm(False)
	    world.setThundering(False)

The code above disables weather on the server.

### Commands

Commands can be created by defining a function with the command name and then registering it as shown in the [example plugin](https://github.com/moonymax/pyhook/blob/master/installer/pyplugins/sampleplugin.py)

## Usage

Py4J is the foundation of this plugin, for more details on how you can interact with the java runtime checkout the [Py4J FAQ](https://www.py4j.org/faq.html) or the [Py4J docs](https://www.py4j.org/contents.html) in general.

## Known Issues

Errors within a plugin script file have to be handled in a try except otherwise they result in a silent failure.
