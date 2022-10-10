from py4j.java_gateway import JavaGateway, CallbackServerParameters, Py4JNetworkError
import importlib.util
import os
import time
import logging

logging.basicConfig(filename='pyhook.log', filemode='w',
                    format='%(levelname)s - %(message)s')

specs = {}
plugins = {}
scriptsPath = 'pyplugins/'

javaPluginRef = None

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

    def __init__(self, gateway):
        self.gateway = gateway

    def onEvent(self, event):
        if(event == "stop"):
            self.gateway.shutdown()
            global stop
            stop = True
            return
        if(event.getEventName() == 'onCommand'):
            sender = event.getSender()
            name = event.getName()
            args = event.getArgs()
            callplugins('on'+(name.capitalize())+'Cmd', gateway=self.gateway,
                        pyhook=javaPluginRef, sender=sender, name=name, arguments=args)
            return
        callplugins(event.getEventName(), gateway=self.gateway,
                    pyhook=javaPluginRef, event=event)
        return event

    class Java:
        implements = ["com.moonymax.pyhook.EventListener"]


# if __name__ == "__main__":

gateway = JavaGateway(
    callback_server_parameters=CallbackServerParameters())
while not stop:
    try:
        gateway.jvm.System.getProperty("java.runtime.name")
        print('JVM accepted connection')
        listener = PythonListener(gateway)
        javaPluginRef = gateway.entry_point.registerListener(listener)
        callplugins('onEnable', gateway=gateway, pyhook=javaPluginRef)
        stop = True
    except Py4JNetworkError:
        print('No JVM listenting')
        time.sleep(1)
    except Exception:
        gateway.shutdown()
        stop = True
        pass
#gateway.jvm.System.out.println("Hello from python!")


# gateway.entry_point.notifyAllListeners()
# gateway.shutdown()
