{
  'variables' : {
    'node_bin_dir': '<!(npm bin)',
    'tsc': '<(node_bin_dir)/tsc',
    'tslint': '<(node_bin_dir)/tslint',
    'blpapits_src': '<(module_root_dir)/blpapi.ts'
  },
  'targets' : [
    {
      # Compile typescript code
      'target_name': 'tsc',
      'type': 'none',
      'dependencies': ['copy_dts'],
      'sources': ['<(blpapits_src)'],
      'rules': [
        {
          'rule_name': 'ts_comp',
          'extension': 'ts',
          'outputs': [
            '<(module_root_dir)/<(RULE_INPUT_ROOT).js'
          ],
          'action': [
            '<(tsc)', '--module', 'commonjs', '--target', 'ES5',
            '--noImplicitAny', '--noEmitOnError', '--sourceMap',
            '<(RULE_INPUT_PATH)'
          ]
        }
      ],
    },
    {  'target_name': 'copy_dts',
       'type': 'none',
        # Copy 'blapijs' typescript definition files to the build directory,
        # this is necessary to be able to import the module from typescript.
        'copies': [
          {
            'files': ['<(module_root_dir)/etc/blpapijs.d.ts'],
            'destination': '<(PRODUCT_DIR)'
          }
        ]
    },
    {
      # Run tslint, uses a dummy output file.
      'target_name': 'tslint',
      'type': 'none',
      'actions': [
      {
          'action_name': 'tslint',
          'message': 'Running tslint...',
          'inputs': ['<(module_root_dir)/blpapi.ts'],
          'outputs': ['<(module_root_dir)/.tslint.d'],
          'action': ['sh', '-c', '<(tslint) -f <@(_inputs) && touch <@(_outputs)']
        }
      ]
    },
    {
      'target_name': 'blpapijs',
      'sources': [ 'blpapijs.cpp' ],
      'cflags!': [ '-fno-exceptions' ],
      'cflags_cc!': [ '-fno-exceptions' ],
      'conditions': [
        ['OS=="win"', {
          'include_dirs': [
            '<(module_root_dir)/deps/blpapi/include-3.7.9.1'
          ],
          'msvs_settings': {
            'VCCLCompilerTool': {
              'AdditionalOptions': [ '/EHsc' ]
            }
          },
          'conditions': [
            ['target_arch=="ia32"', {
              'libraries': [
                '<(module_root_dir)/deps/blpapi/win/blpapi3_32.lib'
              ]
            }],
            ['target_arch=="x64"', {
              'libraries': [
                '<(module_root_dir)/deps/blpapi/win/blpapi3_64.lib'
              ]
            }]
          ]
        }],
        ['OS=="linux"', {
          'include_dirs': [
            '<(module_root_dir)/deps/blpapi/include-3.7.9.1'
          ],
          'ldflags': [
            '-Wl,-R<(module_root_dir)/deps/blpapi/linux',
            '-L<(module_root_dir)/deps/blpapi/linux'
          ],
          'conditions': [
            ['target_arch=="ia32"', {
              'libraries': [ '-lblpapi3_32' ]
            }],
            ['target_arch=="x64"', {
              'libraries': [ '-lblpapi3_64' ]
            }]
          ]
        }],
        ['OS=="mac"', {
          'include_dirs': [
            '<(module_root_dir)/deps/blpapi/include-3.8.1.1'
          ],
          'ldflags': [
            '-Wl,-rpath,<(module_root_dir)/deps/blpapi/osx',
            '-L<(module_root_dir)/deps/blpapi/osx'
          ],
          'conditions': [
            ['target_arch=="ia32"', {
              'libraries': [ '-lblpapi3_32' ],
              'xcode_settings': { 'ARCHS': [ 'i386' ] }
            }],
            ['target_arch=="x64"', {
              'libraries': [ '-lblpapi3_64' ],
              'xcode_settings': { 'ARCHS': [ 'x86_64' ] }
            }]
          ],
          'xcode_settings': {
            'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
            'GCC_ENABLE_CPP_RTTI': 'NO',
            'INSTALL_PATH': '@rpath',
            'LD_DYLIB_INSTALL_NAME': '',
            'OTHER_LDFLAGS': [
              '-Wl,-search_paths_first',
              '-Wl,-rpath,<(module_root_dir)/deps/blpapi/osx',
              '-L<(module_root_dir)/deps/blpapi/osx'
            ]
          }
        }]
      ]
    }
  ]
}
