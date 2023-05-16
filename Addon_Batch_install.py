# Informações sobre o addon
bl_info = {
    "name": "Bacth Addon Installer",
    "author": "Yuri Schmaltz",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "File > User Preferences > Addons",
    "description": "Instala todos os addons a partir de uma pasta específica",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
}

# Importação de módulos necessários
import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty
import os

# Classe para as preferências do addon
class AddonInstallerPreferences(AddonPreferences):
    bl_idname = __name__

    # Propriedade para definir a pasta de addons
    addon_directory: StringProperty(
        name="Pasta de Addons",
        subtype='DIR_PATH',
        default=""
    )

    # Método para desenhar a interface do usuário
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "addon_directory")
        layout.operator("wm.addon_batch_install")

# Classe para o operador de instalação em lote de addons
class AddonBatchInstall(Operator):
    bl_idname = "wm.addon_batch_install"
    bl_label = "Instalar Addons em Lote"

    # Método para executar a ação do operador
    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        addon_directory = addon_prefs.addon_directory

        # Função para verificar arquivos recursivamente em subpastas e contar o número de addons encontrados
        def count_files(directory):
            count = 0
            for file in os.listdir(directory):
                filepath = os.path.join(directory, file)
                if os.path.isdir(filepath):
                    count += count_files(filepath)
                elif file.endswith(".py") or file.endswith(".zip"):
                    count += 1
            return count

        num_addons = count_files(addon_directory)

        # Função para verificar arquivos recursivamente em subpastas e instalar addons com barra de progresso
        def check_files(directory, progress):
            for file in os.listdir(directory):
                filepath = os.path.join(directory, file)
                if os.path.isdir(filepath):
                    check_files(filepath, progress)
                elif file.endswith(".py") or file.endswith(".zip"):
                    bpy.ops.preferences.addon_install(filepath=filepath)
                    progress += 1
                    wm.progress_update(progress)

        wm = context.window_manager
        wm.progress_begin(0, num_addons)
        check_files(addon_directory, 0)
        wm.progress_end()

        return {'FINISHED'}

# Funções para registrar e desregistrar classes
def register():
    bpy.utils.register_class(AddonInstallerPreferences)
    bpy.utils.register_class(AddonBatchInstall)

def unregister():
    bpy.utils.unregister_class(AddonBatchInstall)
    bpy.utils.unregister_class(AddonInstallerPreferences)

# Executa o registro das classes quando o script é executado diretamente
if __name__ == "__main__":
    register()