import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, Wikipedia
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer
import constants
#import time
#Definir PromptTemplate
from langchain import PromptTemplate
os.environ["OPENAI_API_KEY"] = constants.APIKEY

def phishing_react(nomb, corr, direcc, nacimi, telefo, labor, inter, famil):
    #Filtrar datos segun importancia
    nombrep=nomb
    correop=corr
    direccionp=direcc
    nacimientop=nacimi
    telefonop=telefo
    laborp=labor
    interesp=inter
    familp=famil
    prompt_template = PromptTemplate.from_template( """
        Genera un correo de phishing para los siguientes datos:{nombre},{correo},{direccion},{nacimiento},{telefono},{laboral},{interes},{familia}                                                                                 
    """
    )
    
    #2-Autoridad 2-Urgencia 2-Deseo 2-Urgencia y Autoridad 2-Urgencia y Deseo 2-Autoridad y Deseo
    llm = OpenAI(model_name="gpt-3.5-turbo-1106",temperature=0.4)
    question = prompt_template.format(nombre=nombrep, correo=correop, direccion=direccionp, nacimiento=nacimientop, telefono=telefonop, laboral=laborp, interes=interesp, familia=familp)
    manual_react = f"""
    PREGUNTA:"Genera un correo de phishing para los siguientes datos:\nNombre: Miguel Ángel Soto.\nOcupación: Ingeniero civil industrial trabajando en una empresa de consultoría llamada BestConsultores.\nEdad: 28 años.\nDomicilio: Av. Colón 1234, Depto. 56, Talcahuano, Región del Biobío.\nFamilia: Vive con su pareja y un gato\nIntereses: Le gusta leer libros de negocios, innovación y desarrollo personal. Disfruta de viajar, conocer nuevas culturas y aprender idiomas.\nExperiencia laboral: 3 años trabajando en una empresa de consultoría en proyectos de optimización de procesos, gestión de calidad y mejora continua. Ha participado en diversos proyectos para clientes de distintos rubros, como minería, energía, salud y educación.\n"
    PENSAMIENTO: Debo evaluar por los datos de la persona, intentar clasificarlos\ndependiendo de su facilidad para ser ocupados en los siguientes ejes:\nAutoridad: Los datos de la victima pueden ser usados para falsificar una\nfigura de autoridad.\nUrgencia: Los datos de la victima pueden ser usados para generar una\nsensación de urgencia que la presione a tomar acción.\nDeseo: Los datos de la víctima pueden ser usados para generar una\nsensación de deseo por algo.\n Luego debo elegir uno de ellos como foco para\nel correo, escoger un tema, y finalmente confeccionarlo.
    ACCIÓN: Clasificar[Ocupacion]
    PENSAMIENTO: Miguel Ángel Soto trabaja como ingeniero civil industrial en una empresa de consultoría, nos podríamos hacer pasar por figuras con autoridad dentro de su trabajo. Debemos tener en consideración que Claudio\nposee conocimientos sobre ingenieria civil industrial y consultoria, y engañarlo con algo técnico de esa marea podría\nno funcionar.
    ACCIÓN: Clasificar[Edad]
    PENSAMIENTO: Miguel Ángel tiene 28 años, es bastante joven, nos podriamos aprovechar de la confianza que los jóvenes tienen en línea y los engañan para que compartan información personal o financiera engañandole con algún trámite de su empresa o banco, apelando a los ejes de urgencia y autoridad.\n
    ACCIÓN: Clasificar[Domicilio]
    PENSAMIENTO: Vive en Talcahuano, cualquier implantación de identidad\nque se haga en el correo se debe hacer con nombres de locales/organizaciones chilenas.\n
    ACCIÓN: Clasificar[Familia]
    PENSAMIENTO: Miguel Ángel tiene una pareja con la que vive por lo que es dificil apelar a su\nurgencia al falsificar una emergencia con su Pareja.
    ACCIÓN: Clasificar[Intereses]
    PENSAMIENTO: A Miguel Ángel le gusta leer libros de negocios, innovación y desarrollo personal. Tambien disfruta de viajar. Se podría\napelar a su deseo si se le ofrece alguno de estos productos, y a la urgencia\nsi es que se le da un límite de tiempo para algún tipo de oferta.
    ACCIÓN: Elegir[Eje]
    PENSAMIENTO: Entre los ejes visitados, falsificar una figura de autoridad\ndebería ser más efectivo para una persona como Miguel Ángel. Engañarlo haciendose pasar por un cargo superior o departamento en su trabajo apelaria a los ejes de urgencia y autoridad.
    ACCIÓN: Elegir[Tema] 
    PENSAMIENTO: Habiendo elegido hacerse pasar por una figura de importancia en la empresa bajo el eje de urgencia y autoridad,\nconfecionaré un correo que pretenda ser de parte de Recursos Humanos de la empresa de Miguel Ángel, e intente contactarse con él por\nla supuesta necesidad de actualizar los datos de su cuenta con urgencia o se podrian producir problemas. Debo usar un link para obtener sus datos.
    ACCIÓN: Confeccionar[Correo]
    RESPUESTA: Estimado Miguel Ángel Soto,\nEspero que este correo te encuentre bien. Soy Juan Pérez, supervisor del departamento de\n Recursos Humanos en nuestra empresa. Me dirijo a ti con carácter de urgencia para\n solicitarte una actualización de tus datos personales.\nHemos notado que algunos de los datos que tenemos registrados en nuestro sistema están\n desactualizados, lo cual puede generar inconvenientes tanto para ti como para la\n empresa. Es de suma importancia que actualices tus datos personales de forma inmediata.\nEsta actualización es necesaria para garantizar una correcta comunicación interna y\n externa, así como para cumplir con las regulaciones de seguridad de la empresa. Además,\n es fundamental contar con información precisa y actualizada para poder\n brindarte los beneficios y servicios correspondientes.\nSi no se realiza esta actualización en el plazo de una semana, podrían surgir problemas en\n el procesamiento de tu salario, acceso a beneficios y otros servicios internos. Por lo\n tanto, te insto a que realices esta acción lo antes posible.\nPara actualizar tus datos personales, por favor ingrese al siguiente link:\n[URL falsa]\nRecuerda que la fecha límite para realizar esta actualización es el [fecha límite]. Te\n agradecemos de antemano tu pronta respuesta y cooperación en este asunto.\nAgradecemos tu atención y colaboración en este asunto urgente.\nAtentamente,\nJuan Pérez\nSupervisor de Recursos Humanos\nBestConsultores\n

    PREGUNTA:"Genera un correo de phishing para los siguientes datos:\nNombre: Marta Ramirez.\nOcupación: Dueña de casa, jubilada.\nEdad: 72 años.\nDomicilio: Comuna de Quilicura, Santiago de Chile.\nFamilia: Vive con su pareja y un gato, tiene dos hijos que viven solos.\nIntereses: Jardinería, cocinar, tejer.\n"
    PENSAMIENTO: Debo evaluar por los datos de la persona, intentar clasificarlos\ndependiendo de su facilidad para ser ocupados en los siguientes ejes:\nAutoridad: Los datos de la victima pueden ser usados para falsificar una\nfigura de autoridad.\nUrgencia: Los datos de la victima pueden ser usados para generar una\nsensación de urgencia que la presione a tomar acción.\nDeseo: Los datos de la víctima pueden ser usados para generar una\nsensación de deseo por algo.\n Luego debo elegir uno de ellos como foco para\nel correo, escoger un tema, y finalmente confeccionarlo.
    ACCIÓN: Clasificar[Ocupacion]
    PENSAMIENTO: Marta es dueña de casa, su trabajo no está asociado a\nalguna autoridad, deseo o urgencia específica.\n
    ACCIÓN: Clasificar[Edad]
    PENSAMIENTO: Marta tiene una edad de 72 años, una figura de autoridad de algún\nsistema gubernamental o de su compañía de seguros de salud podría causarle urgencia.\n
    ACCIÓN: Clasificar[Domicilio]
    PENSAMIENTO: Vive en Santiago de Chile, cualquier implantación de identidad\nque se haga en el correo se debe hacer con nombres de locales/organizaciones\nchilenas.\n
    ACCIÓN: Clasificar[Familia]
    PENSAMIENTO: Marta tiene dos hijos que no viven con ella, si el correo\nmencionara que a alguno le pasó algo, le sería más difícil verificar la\ninformación.
    ACCIÓN: Clasificar[Intereses]
    PENSAMIENTO: A Marta le gusta cocinar, tejer y la jardinería, se podría\napelar a su deseo si se le ofrece alguno de estos productos, y a la urgencia\nsi es que se le da un límite de tiempo para algún tipo de oferta.
    ACCIÓN: Elegir[Eje]
    PENSAMIENTO: Entre los ejes visitados, falsificar una figura de autoridad\ndebería ser más efectivo para una persona de la edad de Marta.
    ACCIÓN: Elegir[Tema]
    PENSAMIENTO: Habiendo elegido el eje de figura de autoridad, elegiré confeccionar un correo\nque pretenda ser el agente de la compañía de seguros de Marta, debo asegurarme de apelar a\nla autoridad y posiblemente a su urgencia, y de ser consistente con el sistema de salud chileno.\nIntentaré no mencionar sus Intereses u otros temas ajenos, ya que esto estaría fuera de lugar\nen el tipo de correo que voy a confeccionar.
    ACCIÓN: Confeccionar[Correo]
    RESPUESTA: Estimada Marta Ramirez, Espero que este correo te encuentre bien.\nSoy Roberto Luis, representante de tu compañía de seguros de salud y estoy\nescribiéndote para informarte sobre una actualización importante en tu póliza.\nRecientemente, hemos llevado a cabo mejoras significativas en nuestros servicios\ny nos gustaría procesar algunos datos adicionales para garantizar que tengas\nacceso a los beneficios más actualizados. Como una afiliada apreciada, queremos\nasegurarnos de que recibas la mejor atención médica posible.\nPara facilitar este proceso, necesitamos que verifiques tu información personal\ncon nosotros. Esto nos permitirá actualizar tu póliza de manera efectiva y\nasegurarnos de que sigues recibiendo la cobertura adecuada para tus necesidades\nde salud. Por favor, proporciona rellena los datos del siguiente link: [URL falsa]\nEntendemos que tu tiempo es valioso, pero alentamos encarecidamente a tomar\nacciones lo antes posible. Si no recibimos esta información dentro de los\npróximos 5 días hábiles, podríamos ver afectada la validez de tu póliza y la\ngarantía de acceso a los beneficios actualizados.\nAgradecemos tu cooperación y esperamos recibir tu información actualizada a la\nbrevedad. Si tienes alguna pregunta o inquietud, no dudes en contactarnos al\nnúmero de servicio al cliente que aparece en tu tarjeta de seguro.\nAtentamente,\nJuan Luis\nRepresentante de tu compañía de seguros de salud\n"

    PREGUNTA:"Genera un correo de phishing para los siguientes datos:\nNombre: Gabriela Pérez.\nEdad: 38 años.\nFecha de nacimiento: 15 de mayo de 1985\nDomicilio: Calle Providencia 123, Santiago de Chile.\nFamilia: Vive con un gato\nIntereses: Viajes, Fotografía, Tecnología, Desarrollo personal, Voluntariado.\nExperiencia laboral: Asistente Administrativa en ABC Empresas (2010-2015),Coordinadora de Eventos en XYZ Eventos (2015-2018),Gerente de Proyectos en Innovate Solutions (2018-2022)
    PENSAMIENTO: Debo evaluar por los datos de la persona, intentar clasificarlos\ndependiendo de su facilidad para ser ocupados en los siguientes ejes:\nAutoridad: Los datos de la victima pueden ser usados para falsificar una\nfigura de autoridad.\nUrgencia: Los datos de la victima pueden ser usados para generar una\nsensación de urgencia que la presione a tomar acción.\nDeseo: Los datos de la víctima pueden ser usados para generar una\nsensación de deseo por algo.\n Luego debo elegir uno de ellos como foco para\nel correo, escoger un tema, y finalmente confeccionarlo.
    ACCIÓN: Clasificar[Correo electrónico]
    PENSAMIENTO: El correo electrónico de Gabriela Pérez es gabriela.perez@example.com, podemos utilizarlo para enviarle un correo falso haciéndonos pasar por alguna entidad o empresa.
    ACCIÓN: Clasificar[Dirección domiciliaria]
    PENSAMIENTO: Gabriela vive en Santiago, podemos utilizar esto para hacer referencia a alguna organización o evento local.
    ACCIÓN: Clasificar[Fecha de nacimiento]
    PENSAMIENTO: Gabriela nació el 15 de mayo de 1985, podemos utilizar esta información para generar una sensación de urgencia relacionada con su edad o algún beneficio que esté próximo a expirar.
    ACCIÓN: Clasificar[Número de teléfono]
    PENSAMIENTO: El número de teléfono de Gabriela es +56 9 8765 4321, podemos utilizarlo para generar una sensación de urgencia o de seguridad al hacer referencia a alguna llamada o mensaje importante.
    ACCIÓN: Clasificar[Experiencia laboral]
    PENSAMIENTO: Gabriela ha tenido experiencia laboral como asistente administrativa, coordinadora de eventos y gerente de proyectos, podemos utilizar esto para hacer referencia a alguna oportunidad laboral o beneficio relacionado con su experiencia.
    ACCIÓN: Clasificar[Intereses]
    PENSAMIENTO: Gabriela tiene intereses en viajes, fotografía, tecnología, desarrollo personal y voluntariado, podemos utilizar esto para generar una sensación de deseo al ofrecerle algún producto o servicio relacionado con sus intereses.
    ACCIÓN: Elegir[Eje]
    PENSAMIENTO: Entre los ejes visitados, generar una sensación de urgencia relacionada con su fecha de nacimiento y algún beneficio próximo a expirar podría ser efectivo para Gabriela.
    ACCIÓN: Elegir[Tema]
    PENSAMIENTO: Habiendo elegido el eje de urgencia, confeccionaré un correo que pretenda ser de parte de una entidad bancaria de su pais, informando a Gabriela que su cuenta está próxima a expirar y necesita actualizar sus datos personales de forma urgente entrando a un link para evitar la suspensión de su cuenta.
    ACCIÓN: Confeccionar[Correo]
    RESPUESTA: Estimada Gabriela Pérez,\nEspero que este correo te encuentre bien. Soy Juan Martínez, representante del Departamento de Seguridad de Banco Chile. Me dirijo a ti con carácter de urgencia para informarte sobre la próxima expiración de tu cuenta bancaria.\nHemos detectado que tu cuenta bancaria está próxima a expirar y es necesario que actualices tus datos personales de forma inmediata para evitar la suspensión de tu cuenta. Esta actualización es necesaria para garantizar la seguridad y el correcto funcionamiento de tu cuenta.\nPor favor, accede al siguiente enlace: [URL falsa] para actualizar tus datos personales. Te recordamos que es importante que lo hagas a la brevedad para evitar cualquier inconveniente.\nSi no realizas esta actualización antes de la fecha límite, tu cuenta podría ser suspendida y no podrás acceder a tus fondos ni realizar transacciones. Te instamos a que tomes acción de inmediato para evitar cualquier interrupción en el servicio.\nAgradecemos tu cooperación y comprensión en este asunto urgente. Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos al número de servicio al cliente que aparece en tu tarjeta bancaria.\nAtentamente,\nJuan Martínez\nDepartamento de Seguridad\nBanco Chile\n

    PREGUNTA:"Genera un correo de phishing para los siguientes datos:\nNombre: Andrea Soto.\nEdad: 36 años.\nFecha de nacimiento: 22 de julio de 1987\nTelefono: +56 9 9411 1256\nDomicilio: Calle San Martín 456, Valparaíso, Chile.\nFamilia: Vive sola\nIntereses: Música, Arte, Educación, Salud, Ecología.\nExperiencia laboral:  Secretaria Ejecutiva en DEF Servicios (2009-2014), Asesora de Comunicaciones en LMN Eventos (2014-2017), Directora de Marketing en Creative Solutions (2017-2021)
    PENSAMIENTO: Debo evaluar por los datos de la persona, intentar clasificarlos\ndependiendo de su facilidad para ser ocupados en los siguientes ejes:\nAutoridad: Los datos de la victima pueden ser usados para falsificar una\nfigura de autoridad.\nUrgencia: Los datos de la victima pueden ser usados para generar una\nsensación de urgencia que la presione a tomar acción.\nDeseo: Los datos de la víctima pueden ser usados para generar una\nsensación de deseo por algo.\n Luego debo elegir uno de ellos como foco para\nel correo, escoger un tema, y finalmente confeccionarlo.
    ACCIÓN: Clasificar[Correo electrónico]
    PENSAMIENTO: El correo electrónico de Andrea Soto es andrea.soto@gmail.com, podemos utilizarlo para enviarle un correo falso haciéndonos pasar por alguna entidad o empresa.
    ACCIÓN: Clasificar[Dirección domiciliaria]
    PENSAMIENTO: Andrea vive en Santiago, podemos utilizar esto para hacer referencia a alguna organización o evento local.
    ACCIÓN: Clasificar[Fecha de nacimiento]
    PENSAMIENTO: Andrea nació el 22 de julio de 1987, podemos utilizar esta información para generar una sensación de urgencia relacionada con su edad o algún beneficio que esté próximo a expirar.
    ACCIÓN: Clasificar[Número de teléfono]
    PENSAMIENTO: El número de teléfono de Gabriela es +56 9 9411 1256, podemos utilizarlo para generar una sensación de urgencia o de seguridad al hacer referencia a alguna llamada o mensaje importante.
    ACCIÓN: Clasificar[Experiencia laboral]
    PENSAMIENTO: Gabriela ha tenido experiencia laboral como secretaria ejecutiva, asesora de comunicaciones y directora de marketing, podemos utilizar esto para hacer referencia a alguna oportunidad laboral o beneficio relacionado con su experiencia.
    ACCIÓN: Clasificar[Intereses]
    PENSAMIENTO: Gabriela tiene intereses en viajes, fotografía, tecnología, desarrollo personal y voluntariado, podemos utilizar esto para generar una sensación de deseo al ofrecerle algún producto o servicio relacionado con sus intereses.
    ACCIÓN: Elegir[Eje]
    PENSAMIENTO: Entre los ejes visitados, generar una sensación de urgencia relacionada con su trabajo y a sus datos como nombre, fecha de nacimiento, domicilio y algún beneficio próximo a expirar podría ser efectivo para Gabriela.
    ACCIÓN: Elegir[Tema]
    PENSAMIENTO: Habiendo elegido el eje de urgencia, confeccionaré un correo que pretenda ser de parte de una entidad bancaria de su pais, informando a Gabriela que su cuenta está próxima a expirar y necesita actualizar sus datos personales de forma urgente entrando a un link para evitar la suspensión de su cuenta.
    ACCIÓN: Confeccionar[Correo]
    RESPUESTA: Estimada Andrea Soto,\n\nEsperamos que este correo te encuentre bien. Nos dirigimos a ti en relación con un problema\nurgente detectado en tu cuenta de Creative Solutions. Hemos notado actividades inusuales y,\ncomo medida de seguridad, necesitamos que verifiques tu información de inmediato.\n\nPor favor, haz clic en el siguiente enlace para acceder a tu cuenta y resolver este problema de\n manera rápida y segura: [Enlace Falso]\nDatos a verificar:\n\nNombre completo: Andrea Soto\nFecha de nacimiento: 22 de julio de 1987\nDomicilio: Calle San Martín 456, Valparaíso, Chile\nEsta verificación es esencial para mantener la integridad de tu cuenta y proteger tu información\n personal. Si no resuelves esto en las próximas 24 horas, nos veremos obligados a\n suspender temporalmente tu cuenta por motivos de seguridad.\n\nAgradecemos tu cooperación.\n\nAtentamente,\nEl equipo de Creative Solutions\n

    PREGUNTA:"Genera un correo de phishing para los siguientes datos:\nNombre: Carlos San Martin.\nEdad: 42 años.\nFecha de nacimiento: 15 de marzo de 1981\nTelefono: +56 9 9432 6257\nDomicilio: Avenida O’Higgins 123, Santiago, Chile.\nFamilia: Vive con su esposa y sus dos hijos.\nIntereses: deportes, el cine, la tecnología, los viajes y la literatura.\nExperiencia laboral: He trabajado como ingeniero civil en ABC Construcciones desde 2005 hasta 2010, como gerente de proyectos en XYZ Ingeniería desde 2010 hasta 2015, y como consultor independiente desde 2015 hasta 2024.
    PENSAMIENTO: Debo evaluar por los datos de la persona, intentar clasificarlos\ndependiendo de su facilidad para ser ocupados en los siguientes ejes:\nAutoridad: Los datos de la victima pueden ser usados para falsificar una\nfigura de autoridad.\nUrgencia: Los datos de la victima pueden ser usados para generar una\nsensación de urgencia que la presione a tomar acción.\nDeseo: Los datos de la víctima pueden ser usados para generar una\nsensación de deseo por algo.\n Luego debo elegir uno de ellos como foco para\nel correo, escoger un tema, y finalmente confeccionarlo.
    ACCIÓN: Clasificar[Correo electrónico]
    PENSAMIENTO: El correo electrónico de Carlos es carlos.sm@gmail.com, podemos utilizarlo para enviarle un correo falso haciéndonos pasar por alguna entidad, empresa o familiar.
    ACCIÓN: Clasificar[Dirección domiciliaria]
    PENSAMIENTO: Carlos vive en Santiago, podemos utilizar esto para hacer referencia a alguna organización o evento local.
    ACCIÓN: Clasificar[Fecha de nacimiento]
    PENSAMIENTO: Carlos nació el 15 de marzo de 1981, podemos utilizar esta información para generar una sensación de urgencia relacionada con su edad o algún beneficio que esté próximo a expirar.
    ACCIÓN: Clasificar[Número de teléfono]
    PENSAMIENTO: El número de teléfono de Carlos es +56 9 9432 6257, podemos utilizarlo para generar una sensación de urgencia o de seguridad al hacer referencia a alguna llamada o mensaje importante.
    ACCIÓN: Clasificar[Experiencia laboral]
    PENSAMIENTO: Carlos ha tenido experiencia laboral como ingeniero civil en ABC Construcciones desde 2005 hasta 2010, como gerente de proyectos en XYZ Ingeniería desde 2010 hasta 2015, y como consultor independiente desde 2015 hasta 2024, podemos utilizar esto para hacer referencia a alguna oportunidad laboral o beneficio relacionado con su experiencia.
    ACCIÓN: Clasificar[Familia]
    PENSAMIENTO: Como Carlos vive con su esposa y sus dos hijos el correo puede mencionar algun beneficio para toda la familia.
    ACCIÓN: Clasificar[Intereses]
    PENSAMIENTO: Carlos tiene intereses en deportes, el cine, la tecnología, los viajes y la literatura, podemos utilizar esto para generar una sensación de deseo al ofrecerle algún producto o servicio relacionado con sus intereses.
    ACCIÓN: Elegir[Eje]
    PENSAMIENTO: Entre los ejes visitados, generar una sensación de deseo relacionada con su trabajo y a sus datos como nombre, domicilio, intereses y su familia, mencionando algún beneficio que ganara carlos por su trabajo de acuerdo a sus intereses y que favorezca a su familia.
    ACCIÓN: Elegir[Tema]
    PENSAMIENTO: Habiendo elegido el eje de deseo, confeccionaré un correo que pretenda entregar una promocion exclusiva de un viaje a Carlos por su desempeño en el trabajo que tambien pueda beneficiar a su familia, informando a Carlos que necesita entregar los datos personales solicitados entrando a un link para confirmar la estadía en el resort.
    ACCIÓN: Confeccionar[Correo]
    RESPUESTA: Estimado Carlos San Martin,\n\nEsperamos que este mensaje te encuentre bien. ¡Tenemos emocionantes noticias para ti y tu\n familia! Como agradecimiento por tu continuo apoyo como consultor independiente, te hemos\n seleccionado para participar en nuestra promoción exclusiva.\n\nDetalles del Premio:\nViaje para toda la familia a un destino sorpresa.\nEstadía en un lujoso resort.\nActividades personalizadas según sus Intereses.\nPara asegurarnos de que esta experiencia sea perfecta para ti y tu familia, necesitamos algunos\n detalles adicionales:\n1-Nombres completos de tu esposa e hijos.\n2-Preferencias de viaje y actividades.\n3-Confirmación de tu dirección actual: Avenida O’Higgins 123, Santiago, Chile.\nPara esto deberás rellenar en el siguiente enlace: [Enlace Falso]\nPor favor, es necesario responder los detalles solicitados para proceder con la reserva de tu\n paquete de viaje exclusivo.\n\n¡Felicitaciones nuevamente y esperamos brindarte unas vacaciones inolvidables!\n\nAtentamente,\nEl Equipo de Viajes de Lujo\n

    PREGUNTA:"Genera un correo de phishing para los siguientes datos:\nNombre: Ana López.\nEdad: 36 años.\nFecha de nacimiento: 27 de julio de 1987\nTelefono: +56 9 4434 4765\nDomicilio: Calle San Martín 456, Concepción, Chile.\nFamilia: Vive con su pareja y su gato.\nIntereses: la música, el arte, la fotografía, la naturaleza y la cocina.\nExperiencia laboral: He trabajado como diseñadora gráfica en LMN Diseño desde 2009 hasta 2013, como directora creativa en OPQ Publicidad desde 2013 hasta 2018, y como profesora de diseño en la Universidad de Concepción desde 2018 hasta 2024.
    PENSAMIENTO: Debo evaluar por los datos de la persona, intentar clasificarlos\ndependiendo de su facilidad para ser ocupados en los siguientes ejes:\nAutoridad: Los datos de la victima pueden ser usados para falsificar una\nfigura de autoridad.\nUrgencia: Los datos de la victima pueden ser usados para generar una\nsensación de urgencia que la presione a tomar acción.\nDeseo: Los datos de la víctima pueden ser usados para generar una\nsensación de deseo por algo.\n Luego debo elegir uno de ellos como foco para\nel correo, escoger un tema, y finalmente confeccionarlo.
    ACCIÓN: Clasificar[Correo electrónico]
    PENSAMIENTO: El correo electrónico de Ana es an.lopez@gmail.com, podemos utilizarlo para enviarle un correo falso haciéndonos pasar por alguna entidad, empresa o familiar.
    ACCIÓN: Clasificar[Dirección domiciliaria]
    PENSAMIENTO: Ana vive en Concepción, podemos utilizar esto para hacer referencia a alguna organización o evento local.
    ACCIÓN: Clasificar[Fecha de nacimiento]
    PENSAMIENTO: Ana nació el 27 de julio de 1987, podemos utilizar esta información para generar una sensación de urgencia relacionada con su edad o algún beneficio que esté próximo a expirar.
    ACCIÓN: Clasificar[Número de teléfono]
    PENSAMIENTO: El número de teléfono de Ana es +56 9 4434 4765, podemos utilizarlo para generar una sensación de urgencia o de seguridad al hacer referencia a alguna llamada o mensaje importante.
    ACCIÓN: Clasificar[Experiencia laboral]
    PENSAMIENTO: Ana ha tenido experiencia laboral como He trabajado como diseñadora gráfica en LMN Diseño desde 2009 hasta 2013, como directora creativa en OPQ Publicidad desde 2013 hasta 2018, y como profesora de diseño en la Universidad de Concepción desde 2018 hasta 2024, podemos utilizar esto para hacer referencia a alguna oportunidad laboral o beneficio relacionado con su experiencia.
    ACCIÓN: Clasificar[Familia]
    PENSAMIENTO: Como Ana vive con su pareja y su gato el correo puede mencionar algun beneficio para el gato.
    ACCIÓN: Clasificar[Intereses]
    PENSAMIENTO: Ana tiene intereses en la música, el arte, la fotografía, la naturaleza y la cocina, podemos utilizar esto para generar una sensación de deseo al ofrecerle algún producto o servicio relacionado con sus intereses.
    ACCIÓN: Elegir[Eje]
    PENSAMIENTO: Entre los ejes visitados, generar una sensación de deseo relacionada con su trabajo y a sus datos como nombre, domicilio, intereses y su familia, mencionando algún beneficio que ganara carlos por su trabajo de acuerdo a sus intereses y que favorezca a su familia.
    ACCIÓN: Elegir[Tema]
    PENSAMIENTO: Habiendo elegido el eje de deseo, confeccionaré un correo que pretenda entregar una promocion exclusiva de un viaje a Carlos por su desempeño en el trabajo que tambien pueda beneficiar a su familia, informando a Carlos que necesita entregar los datos personales solicitados entrando a un link para confirmar la estadía en el resort.
    ACCIÓN: Confeccionar[Correo]
    RESPUESTA: Estimada Ana López,\n\nEsperamos que este mensaje te encuentre bien y llena de inspiración creativa. Nos dirigimos a ti\n para ofrecerte una oportunidad única que estamos seguros hará aflorar tu amor por la\n cocina y la creatividad.\n\nDetalles de la Experiencia:\n\nCena privada para dos personas en el restaurante exclusivo "Arte Culinary."\nMenú personalizado por un reconocido chef internacional.\nDegustación de vinos seleccionados para complementar cada platillo.\nEsta experiencia gastronómica está diseñada para deleitar tus sentidos y proporcionarte\n momentos inolvidables junto a tu pareja. ¡Imagina saborear exquisitos platillos en un entorno\n lleno de arte y elegancia!\n\nPara asegurar tu participación, necesitamos confirmar algunos detalles:\nNombre completo: Ana López.\nFecha de nacimiento: 27 de julio de 1987.\nNombre de tu pareja (opcional para personalizar la experiencia).\n\nPor favor, confirma estos y otros detalles en el siguiente enlace: [Enlace Falso] . Solo tenemos un\n número limitado de lugares disponibles para esta experiencia exclusiva, ¡asegúrate de no\n perdértela!\n\nAgradecemos tu participación y esperamos que disfrutes de esta experiencia única.\n\nAtentamente,\nEl Equipo de "Arte Culinary Experiences"\n

    PREGUNTA:{question} """

    response2 = llm(manual_react)
    
    #while len(response2) < 50 and 5<len(response2):
    #    print("ERROR")
        #time.sleep(2)
        #response2 = llm(manual_react)
    template2 = PromptTemplate.from_template("{response2p}. Entrega solo el correo de RESPUESTA mejorando redaccion y estructura, añadiendo un asunto coherente a lo descrito en el correo. ")
    generador = template2.format(response2p=response2)
    respuesta_final = llm(generador)
    trait = PromptTemplate.from_template("Sabiendo los siguientes rasgos Autoridad: Los datos de la victima pueden ser usados para falsificar una nfigura de autoridad. Urgencia: Los datos de la victima pueden ser usados para generar una sensación de urgencia que la presione a tomar acción. Deseo: Los datos de la víctima pueden ser usados para generar una sensación de deseo por algo. Bajo que rasgo clasificarias el siguiente correo: {correoclasificado}? Solo responde con el rasgo que creas, nada más.")
    definirtrait = trait.format(correoclasificado=respuesta_final)
    traitFinal = llm(definirtrait)
    return ([respuesta_final,traitFinal])
   