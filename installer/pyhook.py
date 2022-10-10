from tkinter import E
from py4j.java_gateway import JavaGateway, CallbackServerParameters, Py4JNetworkError
from py4j.clientserver import ClientServer, JavaParameters, PythonParameters
import importlib.util
import traceback
import os
import time
import logging

logging.basicConfig(filename='pyhook.log', filemode='w',
                    format='%(levelname)s - %(message)s')

specs = {}
plugins = {}
scriptsPath = 'pyplugins/'

gateway = None

stop = False

for f in os.listdir(scriptsPath):
    if f.endswith('.py'):
        specs[f] = importlib.util.spec_from_file_location(f, scriptsPath + f)
        plugins[f] = importlib.util.module_from_spec(specs[f])
        specs[f].loader.exec_module(plugins[f])


def callplugins(functionname, **args):
    for plugin in plugins:
        try:
            function = getattr(plugins[plugin], functionname)
            function(**args)
        except Exception:
            pass


class PythonListener(object):

    def __init__(self):
        pass

    def onEvent(self, pluginRef, eventName, event):
        try:
            global gateway
            if(eventName == "stop"):
                self.gateway.shutdown()
                global stop
                stop = True
                return
            if(eventName == "EnableEvent"):
                callplugins('onEnable', plugin=pluginRef, gateway=gateway)
                return

            if(eventName == 'CommandEvent'):
                sender = event.getSender()
                name = event.getName()
                args = event.getArgs()
                callplugins('on'+(name.capitalize())+'Cmd',
                            plugin=pluginRef, gateway=gateway, sender=sender, name=name, arguments=args)
                return
            if(eventName == "SpigotEvent"):
                callplugins(event.getEventName(),
                            plugin=pluginRef, gateway=gateway, event=event)
        except Exception as e:
            print(e)
        return event

    class Java:
        implements = ["com.moonymax.pyhook.EventListener"]


# if __name__ == "__main__":
def main():
    global stop
    global gateway
    listener = PythonListener()
    gateway = ClientServer(
        java_parameters=JavaParameters(),
        python_parameters=PythonParameters(),
        python_server_entry_point=listener
        # callback_server_parameters=CallbackServerParameters()
    )


"""
    while not stop:
        try:
            gateway.jvm.System.getProperty("java.runtime.name")
            print('JVM accepted connection')
            global javaPluginRef
            javaPluginRef = gateway.entry_point.registerListener(listener)
            stop = True
        except Py4JNetworkError:
            print('No JVM listenting')
            time.sleep(1)
        except Exception:
            gateway.shutdown()
            stop = True
            pass
    # gateway.jvm.System.out.println("Hello from python!")

    # gateway.entry_point.notifyAllListeners()
    # gateway.shutdown()
    """


main()
